import dist
import re


"""
    Convert a PDDL domain into a PROLOG domain.
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
        self.actions = []


class Dual:
    def __init__(self):
        self.pos = []
        self.neg = []


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


def parsepddldomain(pddl):
    ignorelist = [' ', '\n', '\t']

    (_, content, _) = dist.extractsection(pddl, '(', ')')
    (define, domain, content) = dist.extractsection(content, '(', ')')
    (_, requirments, content) = dist.extractsection(content, '(', ')')
    (_, types, content) = dist.extractsection(content, '(', ')')
    (_, predicates, content) = dist.extractsection(content, '(', ')')

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
    parseddomain.actions = actions

    return parseddomain


def constructparameters(parameters, situation):
    convertparams = map(lambda (paramid, paramtype): str.upper(paramid + "_" + paramtype), parameters)
    return "(" + ", ".join(convertparams + [situation]) + ")"


def renamelist(paramlist, paramdict):
    return map(lambda param: str.upper(param + "_" + paramdict[param]), paramlist)


def constructaxioms(axioms, paramdict):
    posprecaxioms, negprecaxioms = axioms
    renamedposaxioms = map(lambda (name, paramlist): (name, renamelist(paramlist, paramdict)), posprecaxioms)
    renamednegaxioms = map(lambda (name, paramlist): (name, renamelist(paramlist, paramdict)), negprecaxioms)
    convertedposaxioms = map(lambda (name, paramlist): name + "(" + ", ".join(paramlist + ['S']) + ")", renamedposaxioms)
    convertednegaxioms = map(lambda (name, paramlist): "not " + name + "(" + ", ".join(paramlist + ['S']) + ")", renamednegaxioms)
    convertedaxioms = convertedposaxioms + convertednegaxioms
    return ", ".join(convertedaxioms) + "."


def constructpreconditions(action):
    posprecaxioms = action.preclist.pos
    negprecaxioms = action.preclist.neg
    prec = ""
    if posprecaxioms or negprecaxioms:
        prec += "poss(" + action.actionname + constructparameters(action.paramlist, 'S') + ") :- " \
                + constructaxioms((posprecaxioms, negprecaxioms), action.paramdict) + "\n\n"
    return prec


def constructposeffects(action):
    # implement a set to keep discontiguous information
    poseffaxioms = action.efflist.pos
    poseffstr = ""
    for poseff in poseffaxioms:
        poseffparams = map(lambda paramid: (paramid, action.paramdict[paramid]), poseff[1])
        poseffstr += poseff[0] + constructparameters(poseffparams, '[A|S]') + " :- A = " \
               + action.actionname + constructparameters(action.paramlist, 'S') + ".\n\n"
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
    efflist = []

    negeff = ""
    negeffdict = {}

    fluentset = set()

    for action in parseddomain.actions:
        #actionset.add((action.actionname, len(action.paramlist)))

        preclist.append(constructpreconditions(action))
        posefflist.append(constructposeffects(action))

        # negative effect collector... how should different parameter names be handled?
        # implement a set to keep discontiguous information
        negeffdict.update(buildnegeffdict(action))


    #print fluentset

    #print negeffdict

    # This doesn't account for parameters that exists in the action parameters,
    # but not the fluent parameters...
    # And, the parameters are not guaranteed to match.

    for negeffkey in negeffdict:
        negefflist.append(negeffkey + constructparameters(negeffdict[negeffkey][0], '[A|S]') + " :- " \
              + ", ".join(map(lambda action: "not A = " + action.actionname
                                             + constructparameters(action.paramlist, 'S'),
                              negeffdict[negeffkey][1])) + ", " \
              + negeffkey + constructparameters(negeffdict[negeffkey][0], 'S') + ".\n\n")

    precstr = "".join(preclist)
    poseffstr = "".join(posefflist)
    negeffstr = "".join(negefflist)
    effstr = poseffstr + "\n\n" + negeffstr

    return precstr + "\n\n" + effstr


path = "/Users/aldendino/Documents/School/SitCalc/Alden/Documents/Res/AIPS-2000DataFiles/2000-Tests/Blocks/Track1/Typed/domain.pddl"
#path = "/Users/aldendino/Documents/School/SitCalc/Alden/Documents/Res/AIPS-2000DataFiles/2000-Tests/Logistics/Track1/Typed/domain.pddl"
#path = "/Users/aldendino/Documents/School/SitCalc/Alden/Documents/workspace/d28/original/domain-28.pddl"

with open(path) as file:
    text = file.read()
    domain = parsepddldomain(text)
    print constructprolog(domain)

