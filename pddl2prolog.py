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
    parsedaction.actionname = actionname.replace('-', '_')
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


def constructdynamic(typeslist):
    dynamiclist = []
    typesset = set()
    for (name, namelist) in typeslist:
        levellist = []
        if name not in typesset:
            levellist.append(name)
            typesset.add(name)
        for item in namelist:
            if item not in typesset:
                levellist.append(item)
                typesset.add(item)
        dynamiclist.append(":- dynamic {0}.".format(", ".join(map(lambda name: name + "/1", levellist))))
    #typessetsorted = sorted(typesset)
    #return map(lambda name: ":- dynamic {0}/1.".format(name), typessetsorted)
    return dynamiclist


def constructtypes(typeslist):
    # Note, this will ignore types which have an empty list, i.e. ('type', [])
    return map(lambda (name, namelist): "\n".join(map(lambda item: "{0}(X) :- {1}(X).".format(name, item), namelist)), typeslist)


def convertparamname(paramid, paramtype):
    return str.upper(paramid + "_" + paramtype)


def constructparameters(parameters, situation):
    convertparams = map(lambda (paramid, paramtype): convertparamname(paramid, paramtype), parameters)
    if situation:
        sit = [situation]
    else:
        sit = []
    return "(" + ", ".join(convertparams + sit) + ")"


def renamelist(paramlist, paramdict):
    return map(lambda param: convertparamname(param, paramdict[param]), paramlist)


"""
    Split a list into two, based on whether a condition is met or not
"""
def splitlist(totallist, cond):
    condtrue, condfalse = [], []
    map(lambda value: (condtrue, condfalse)[not cond(value)].append(value), totallist)
    return condtrue, condfalse


def constructequalities(eqlists, param, paramset, paramdict):
    templist = []
    formatting = lambda valstr, (x, y): "{0}{1} {2} {3}".format(valstr, convertparamname(x, paramdict[x]), "=", convertparamname(y, paramdict[y]))
    posstr = ""
    negstr = "not "
    # check all possible arrangements in both the equalities and inequalities
    for paramother in paramset:
        if (param, paramother) in eqlists.pos:
            templist.append(formatting(posstr, (param, paramother)))
        if (param, paramother) in eqlists.neg:
            templist.append(formatting(negstr, (param, paramother)))
        if (paramother, param) in eqlists.pos:
            templist.append(formatting(posstr, (paramother, param)))
        if (paramother, param) in eqlists.neg:
            templist.append(formatting(negstr, (paramother, param)))
    return templist


def constructaxiomshelper(axioms, paramdict, paramset, combinedaxioms, eqlists, valstr):
    for name, paramlist in axioms:
        for paramid in paramlist:
            if paramid not in paramset:
                paramtype = paramdict[paramid]
                combinedaxioms.append("{0}({1})".format(paramtype, convertparamname(paramid, paramtype)))
                paramset.add(paramid)
                # check if need to add any equalities or inequalities based on the newly added paramid
                combinedaxioms.extend(constructequalities(eqlists, paramid, paramset, paramdict))
        combinedaxioms.append("{0}{1}({2})".format(valstr, name, ", ".join(renamelist(paramlist, paramdict) + ['S'])))


def constructaxioms(axioms, paramdict):
    func = Dual()
    eq = Dual()
    eqcond = lambda x: x[0] == '='
    eq.pos, func.pos = splitlist(axioms.pos, eqcond)
    eq.neg, func.neg = splitlist(axioms.neg, eqcond)

    eqlists = Dual()
    eqtotup = lambda (name, paramlist): (paramlist[0], paramlist[1])
    eqlists.pos = map(eqtotup, eq.pos)
    eqlists.neg = map(eqtotup, eq.neg)

    combinedaxioms = []
    paramset = set()

    posstr = ""
    negstr = "not "
    constructaxiomshelper(func.pos, paramdict, paramset, combinedaxioms, eqlists, posstr)
    constructaxiomshelper(func.neg, paramdict, paramset, combinedaxioms, eqlists, negstr)

    return ", ".join(combinedaxioms)


def constructpreconditions(action):
    prec = ""

    if action.preclist.pos or action.preclist.neg:
        prec += "poss(" + action.actionname + constructparameters(action.paramlist, None) + ", S) :- " \
                + constructaxioms(action.preclist, action.paramdict) + "."
    return prec


def constructposeffects(action):
    # implement a set to keep discontiguous information
    poseffaxioms = action.efflist.pos
    poseffstr = ""
    for poseff in poseffaxioms:
        axiomslist = []
        paramtypeslist = []
        for param in action.paramlist:
            paramid = param[0]
            paramtype = action.paramdict[paramid]
            paramtypeslist.append("{0}({1})".format(paramtype, convertparamname(paramid, paramtype)))
        poseffparams = map(lambda paramid: (paramid, action.paramdict[paramid]), poseff[1])
        axiomlist = paramtypeslist + ["A = " + action.actionname + constructparameters(action.paramlist, None)]
        poseffstr += poseff[0] + constructparameters(poseffparams, '[A|S]') + " :- " + ", ".join(axiomlist) + "."
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


def syncnegeffdicts(resultdict, syncdict):
    for key in syncdict.keys():
        if key in resultdict:
            resultdict[key][1].extend(syncdict[key][1])
        else:
            resultdict[key] = syncdict[key]


def constructprolog(parseddomain):
    preclist = []
    posefflist = []
    negefflist = []

    negeffdict = {}

    typeslist = parseddomain.types

    dynamicstr = "\n".join(constructdynamic(typeslist))

    typesstr = "\n".join(constructtypes(typeslist))

    discontiguous = set()

    for action in parseddomain.actions:
        discontiguous = discontiguous.union(determinediscontiguous(action))

        preclist.append(constructpreconditions(action))

        posefflist.append(constructposeffects(action))

        syncnegeffdicts(negeffdict, buildnegeffdict(action))

    discstr = "\n".join(map(lambda (name, length): ":- dynamic " + name + "/" + str(length) + ".", sorted(discontiguous)))


    for negeffkey in negeffdict:
        paramset = set()
        axiomlist = []
        for action in negeffdict[negeffkey][1]:
            for paramid, paramtype in action.paramlist:
                if paramid not in paramset:
                    axiomlist.append("{0}({1})".format(paramtype, convertparamname(paramid, paramtype)))
                    paramset.add(paramid)
            axiomlist.append("not A = " + action.actionname + constructparameters(action.paramlist, None))
        axiomlist.append(negeffkey + constructparameters(negeffdict[negeffkey][0], 'S'))
        negefflist.append(negeffkey + constructparameters(negeffdict[negeffkey][0], '[A|S]') + " :- " + ", ".join(axiomlist) + ".")

    # Put it all together
    precstr = "\n\n".join(preclist)
    poseffstr = "\n\n".join(posefflist)
    negeffstr = "\n\n".join(negefflist)

    preccomm = "% Preconditions"
    poseffcomm = "% Positive Effects"
    negeffcomm = "% Negative Effects"

    return "\n\n\n".join(filter(lambda string: string, [discstr, dynamicstr, typesstr, preccomm, precstr,
                                                        poseffcomm, poseffstr, negeffcomm, negeffstr]))


"""
    File manipulation
"""


def createprologfrompddl(inpath, outpath):
    inpath = os.path.expanduser(inpath)
    outpath = os.path.expanduser(outpath)
    if not os.path.isfile(inpath):
        raise IOError("Cannot open file " + inpath)
    if not os.path.isdir(outpath):
        raise IOError("Cannot open folder " + outpath)

    infilename = os.path.basename(inpath)
    print infilename
    outfilename = infilename.split('.')[0] + '.pl'
    print outfilename
    outfilepath = os.path.join(outpath, outfilename)
    print outfilepath

    with open(inpath, 'r') as infile:
        pddl = infile.read()
        prolog = constructprolog(parsepddldomain(pddl))
    with open(outfilepath, 'w') as outfile:
        outfile.write(prolog)

parser = argparse.ArgumentParser(description='Convert pddl domain into prolog domain.')
parser.add_argument('inpath', type=str, help='The input path to a pddl domain file.')
parser.add_argument('outpath', type=str, help='The output path to a prolog domain file.')
args = parser.parse_args()

createprologfrompddl(args.inpath, args.outpath)
