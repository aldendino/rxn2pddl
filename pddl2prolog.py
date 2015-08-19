import dist
import re
import os
import argparse


"""
    Convert a PDDL domain into a PROLOG domain.
"""


"""
    Classes for sanity's sake
"""

class Action:
    def __init__(self):
        self.actionname = "unknown"
        self.paramlist = []
        self.paramdict = {}
        self.preclist = []
        self.efflist = []


class Domain:
    def __init__(self):
        self.domainname = "unknown"
        self.types = []
        self.actions = []


class Dual:
    def __init__(self):
        self.pos = []
        self.neg = []


"""
    Parsing tools
"""


def sanitizechars(text, list):
    sanitized = ""
    for i in range(0, len(text)):
        if text[i] not in list:
            sanitized += text[i]
    return sanitized


def sanitizeparams(paramlist):
    return map(lambda param: param[1:], paramlist)


def parseaxiom(axiomstr):
    lists = Dual()
    # Separate axioms based on whether they are negated or not,
    # and place them in the appropriate list.
    if axiomstr.startswith("not"):
        # Account for the negation being applied to multiple axioms.
        # Note that this does not account for any further nested negations.
        section = dist.extractsection(axiomstr, '(', ')')
        while section is not None:
            _, axiom, content = section
            listitems = re.split(r' |\n|\t', axiom)
            lists.neg.append((listitems[0], sanitizeparams(listitems[1:])))
            section = dist.extractsection(content, '(', ')')
    else:
        listitems = re.split(r' |\n|\t', axiomstr)
        lists.pos.append((listitems[0], sanitizeparams(listitems[1:])))
    return lists


def parselist(liststr):
    lists = Dual()
    ## Separate axioms based on whether they are in an and or not,
    # then break the axiom or axioms into positive and negative lists.
    if liststr.startswith("and"):
        # Account for the and being applied to multiple axioms.
        # Note that this does not account for any further nested ands.
        section = dist.extractsection(liststr, '(', ')')
        while section is not None:
            _, axiom, content = section
            parsed = parseaxiom(axiom)
            lists.pos.extend(parsed.pos)
            lists.neg.extend(parsed.neg)
            section = dist.extractsection(content, '(', ')')
    else:
        parsed = parseaxiom(liststr)
        lists.pos.extend(parsed.pos)
        lists.neg.extend(parsed.neg)
    return lists


def parseaction(action, ignorelist):
    action = dist.removeleadingchars(action, ignorelist)
    action = dist.removeleadingstring(action, ":action")
    action = dist.removeleadingchars(action, ignorelist)
    actionname, action = dist.readuntilchars(action, ignorelist)

    action = dist.removeleadingchars(action, ignorelist)
    action = dist.removeleadingstring(action, ":parameters")
    action = dist.removeleadingchars(action, ignorelist)
    _, parameters, action = dist.extractsection(action, '(', ')')
    splitlist = re.split(r' |\n|\t', parameters)
    splitlist = filter(lambda item: item != '', splitlist)
    paramlist = []
    paramdict = {}
    while splitlist:
        paramid = splitlist.pop(0)[1:]
        dash = splitlist.pop(0)
        paramtype = splitlist.pop(0)
        paramlist.append((paramid, paramtype))
        paramdict[paramid] = paramtype

    action = dist.removeleadingchars(action, ignorelist)
    action = dist.removeleadingstring(action, ":precondition")
    action = dist.removeleadingchars(action, ignorelist)
    _, precondition, action = dist.extractsection(action, '(', ')')
    preclist = parselist(precondition)

    action = dist.removeleadingchars(action, ignorelist)
    action = dist.removeleadingstring(action, ":effect")
    action = dist.removeleadingchars(action, ignorelist)
    _, effect, action = dist.extractsection(action, '(', ')')
    efflist = parselist(effect)

    parsedaction = Action()
    parsedaction.actionname = actionname
    parsedaction.paramlist = paramlist #list for ordering
    parsedaction.paramdict = paramdict #dict for quick lookup
    parsedaction.preclist = preclist #Dual
    parsedaction.efflist = efflist #Dual

    return parsedaction


def parsetypes(typestr):
    typeslist = []

    itemlist = filter(lambda item: item != '', re.split(r' |\t|\n', typestr))
    templist = []
    dashflag = False

    for item in itemlist:
        if item == '-':
            dashflag = True
        else:
            if dashflag:
                typeslist.append((item, templist))
                templist = []
                dashflag = False
            else:
                templist.append(item)

    # Catch the case where there is no type hierarchy
    if templist:
        typeslist.extend(map(lambda item: (item, []), templist))

    return typeslist


def parsepddldomain(pddl):
    ignorelist = [' ', '\n', '\t']

    (_, content, _) = dist.extractsection(pddl, '(', ')')
    (define, domain, content) = dist.extractsection(content, '(', ')')
    (_, requirments, content) = dist.extractsection(content, '(', ')')
    (_, types, content) = dist.extractsection(content, '(', ')')
    (_, predicates, content) = dist.extractsection(content, '(', ')')

    types = dist.removeleadingchars(types, ignorelist)
    types = dist.removeleadingstring(types, ":types")
    types = dist.removeleadingchars(types, ignorelist)
    typeslist = parsetypes(types)

    actionlist = []
    section = dist.extractsection(content, '(', ')')
    while section is not None:
        (_, action, content) = section
        actionlist.append(action)
        section = dist.extractsection(content, '(', ')')

    define = dist.removeleadingchars(define, ignorelist)
    dist.removeleadingstring(define, "define")

    domain = dist.removeleadingchars(domain, ignorelist)
    domain = dist.removeleadingstring(domain, "domain")
    domain = dist.removeleadingchars(domain, ignorelist)
    domainname = domain

    actions = []
    for action in actionlist:
        actions.append(parseaction(action, ignorelist))

    parseddomain = Domain()
    parseddomain.domainname = domainname
    parseddomain.types = typeslist
    parseddomain.actions = actions

    return parseddomain


"""
    Constructing tools
"""


def determinediscontiguous(action):
    disc = set()
    # + 1 since the situation parameter will be added.
    for item in action.efflist.pos:
        disc.add((item[0], len(item[1]) + 1))
    for item in action.efflist.neg:
        disc.add((item[0], len(item[1]) + 1))
    return disc


def constructtypes(typeslist):
    # Note, this will ignore types which have an empty list, i.e. ('type', [])
    return map(lambda (name, namelist): "\n".join(map(lambda item: "{0}(X) :- {1}(X).".format(name, item), namelist)), typeslist)


def convertparamname(paramid, paramtype):
    return str.upper(paramid + "_" + paramtype)


def constructparameters(parameters, situation):
    convertparams = map(lambda (paramid, paramtype): convertparamname(paramid, paramtype), parameters)
    return "(" + ", ".join(convertparams + [situation]) + ")"


def renamelist(paramlist, paramdict):
    return map(lambda param: convertparamname(param, paramdict[param]), paramlist)


def constructaxioms(axioms, paramdict):
    convertedaxioms = Dual()
    convertedaxioms.pos = map(lambda (name, paramlist): "{0}({1})".format(name, ", ".join(renamelist(paramlist, paramdict) + ['S'])), axioms.pos)
    convertedaxioms.neg = map(lambda (name, paramlist): "not {0}({1})".format(name, ", ".join(renamelist(paramlist, paramdict) + ['S'])), axioms.neg)
    combinedaxioms = convertedaxioms.pos + convertedaxioms.neg
    for axiom in combinedaxioms:
        print axiom
    return ", ".join(combinedaxioms)


def constructpreconditions(action):
    prec = ""
    if action.preclist.pos or action.preclist.neg:
        prec += "poss(" + action.actionname + constructparameters(action.paramlist, 'S') + ") :- " \
                + constructaxioms(action.preclist, action.paramdict) + ".\n"
    return prec


def constructposeffects(action):
    # implement a set to keep discontiguous information
    poseffaxioms = action.efflist.pos
    poseffstr = ""
    for poseff in poseffaxioms:
        poseffparams = map(lambda paramid: (paramid, action.paramdict[paramid]), poseff[1])
        poseffstr += poseff[0] + constructparameters(poseffparams, '[A|S]') + " :- A = " \
               + action.actionname + constructparameters(action.paramlist, 'S') + ".\n"
    return poseffstr


def buildnegeffdict(action):
    negeffdict = {}
    negeffaxioms = action.efflist.neg
    for negeff in negeffaxioms:
        if negeff[0] in negeffdict:
            negeffdict[negeff[0]][1].append(action)
        else:
            renamednegeff = map(lambda paramid: (paramid, action.paramdict[paramid]), negeff[1])
            negeffdict[negeff[0]] = (renamednegeff, [action])
    return negeffdict


def constructprolog(parseddomain):
    preclist = []
    posefflist = []
    negefflist = []

    negeffdict = {}

    typesstr = "\n".join(constructtypes(parseddomain.types))

    discontiguous = set()

    for action in parseddomain.actions:
        discontiguous = discontiguous.union(determinediscontiguous(action))

        preclist.append(constructpreconditions(action))

        posefflist.append(constructposeffects(action))

        # negative effect collector... how should different parameter names be handled?
        # implement a set to keep discontiguous information
        negeffdict.update(buildnegeffdict(action))

    discstr = "\n".join(map(lambda (name, length): ":- dynamic " + name + "/" + str(length) + ".", sorted(discontiguous)))

    # This doesn't account for parameters that exists in the action parameters,
    # but not the fluent parameters...
    # And, the parameters are not guaranteed to match.

    for negeffkey in negeffdict:
        negefflist.append(negeffkey + constructparameters(negeffdict[negeffkey][0], '[A|S]') + " :- " \
              + ", ".join(map(lambda action: "not A = " + action.actionname
                                             + constructparameters(action.paramlist, 'S'),
                              negeffdict[negeffkey][1])) + ", " \
              + negeffkey + constructparameters(negeffdict[negeffkey][0], 'S') + ".\n")

    precstr = "\n".join(preclist)
    poseffstr = "\n".join(posefflist)
    negeffstr = "\n".join(negefflist)
    effstr = poseffstr + "\n" + negeffstr

    return "\n\n".join([discstr, typesstr, precstr, effstr])


"""
    File manipulation
"""


def createprologfrompddl(inpath, outpath):
    inpath = os.path.expanduser(inpath)
    outpath = os.path.expanduser(outpath)
    if not os.path.isfile(inpath):
        raise IOError("Cannot open file " + inpath)
    with open(inpath, 'r') as infile:
        pddl = infile.read()
        prolog = constructprolog(parsepddldomain(pddl))
    with open(outpath, 'w') as outfile:
        outfile.write(prolog)


#path = "/Users/aldendino/Documents/School/SitCalc/Alden/Documents/Res/AIPS-2000DataFiles/2000-Tests/Blocks/Track1/Typed/domain.pddl"
#path = "/Users/aldendino/Documents/School/SitCalc/Alden/Documents/Res/AIPS-2000DataFiles/2000-Tests/Logistics/Track1/Typed/domain.pddl"
path = "/Users/aldendino/Documents/School/SitCalc/Alden/Documents/workspace/d28/original/domain-28.pddl"

out = "/Users/aldendino/Desktop/out.pl"


#parser = argparse.ArgumentParser(description='Convert pddl domain into prolog domain.')
#parser.add_argument('inpath', type=str, help='The input path to a pddl domain file.')
#parser.add_argument('outpath', type=str, help='The output path to a prolog domain file.')
#args = parser.parse_args()

#createprologfrompddl(args.inpath, args.outpath)

createprologfrompddl(path, out)

