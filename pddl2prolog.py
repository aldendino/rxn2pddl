import dist
import re


"""
    Convert a PDDL domain into a PROLOG domain.
"""


class Action:
    def __init__(self):
        self.actionname = None
        self.paramlist = None
        self.paramdict = None
        self.preclist = None
        self.efflist = None


class Domain:
    def __init__(self):
        self.domainname = None
        self.actions = None


def sanitizechars(text, list):
    sanitized = ""
    for i in range(0, len(text)):
        if text[i] not in list:
            sanitized += text[i]
    return sanitized


def sanitizeparams(paramlist):
    return map(lambda param: param[1:], paramlist)


def parseaxiom(axiomstr):
    poslist = []
    neglist = []
    if axiomstr.startswith("not"):
        section = dist.extractsection(axiomstr, '(', ')')
        while section is not None:
            _, axiom, content = section
            listitems = re.split(r' |\n|\t', axiom)
            neglist.append((listitems[0], sanitizeparams(listitems[1:])))
            section = dist.extractsection(content, '(', ')')
    else:
        listitems = re.split(r' |\n|\t', axiomstr)
        poslist.append((listitems[0], sanitizeparams(listitems[1:])))
    return poslist, neglist


def parselist(liststr):
    posaxiomlist = []
    negaxiomlist = []
    if liststr.startswith("and"):
        section = dist.extractsection(liststr, '(', ')')
        while section is not None:
            _, axiom, content = section
            parsed = parseaxiom(axiom)
            posaxiomlist.extend(parsed[0])
            negaxiomlist.extend(parsed[1])
            section = dist.extractsection(content, '(', ')')
    else:
        parsed = parseaxiom(liststr)
        posaxiomlist.extend(parsed[0])
        negaxiomlist.extend(parsed[1])
    return posaxiomlist, negaxiomlist


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
    parsedaction.preclist = preclist #2-tuple (+, -)
    parsedaction.efflist = efflist #2-tuple (+, -)

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
    posprecaxioms, negprecaxioms = action.preclist
    prec = ""
    if posprecaxioms or negprecaxioms:
        prec += "poss(" + action.actionname + constructparameters(action.paramlist, 'S') + ") :- " \
                + constructaxioms((posprecaxioms, negprecaxioms), action.paramdict) + "\n\n"
    return prec


def constructposeffects(action):
    # implement a set to keep discontiguous information
    poseffaxioms, negeffaxioms = action.efflist
    poseffstr = ""
    for poseff in poseffaxioms:
        poseffparams = map(lambda paramid: (paramid, action.paramdict[paramid]), poseff[1])
        poseffstr += poseff[0] + constructparameters(poseffparams, '[A|S]') + " :- A = " \
               + action.actionname + constructparameters(action.paramlist, 'S') + ".\n\n"
    return poseffstr


def constructprolog(parseddomain):
    preclist = []
    posefflist = []
    negefflist = []
    efflist = []

    negeff = ""
    negeffdict = {}

    #actionset = set()

    for action in parseddomain.actions:
        #actionset.add((action.actionname, len(action.paramlist)))

        preclist.append(constructpreconditions(action))
        posefflist.append(constructposeffects(action))

        # negative effect collector... how should different parameter names be handled?
        # implement a set to keep discontiguous information
        poseffaxioms, negeffaxioms = action.efflist
        for negeff in negeffaxioms:
            if negeff[0] in negeffdict:
                negeffdict[negeff[0]][1].append(action)
            else:
                renamednegeff = map(lambda paramid: (paramid, action.paramdict[paramid]), negeff[1])
                negeffdict[negeff[0]] = (renamednegeff, [action])

    #print actionset

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

    precstr = ""
    for item in preclist:
        precstr += item

    poseffstr = ""
    for item in posefflist:
        poseffstr += item

    negeffstr = ""
    for item in negefflist:
        negeffstr += item

    effstr = poseffstr + "\n\n" + negeffstr

    print precstr
    print effstr


#path = "/Users/aldendino/Documents/School/SitCalc/Alden/Documents/Res/AIPS-2000DataFiles/2000-Tests/Blocks/Track1/Typed/domain.pddl"
#path = "/Users/aldendino/Documents/School/SitCalc/Alden/Documents/Res/AIPS-2000DataFiles/2000-Tests/Logistics/Track1/Typed/domain.pddl"
path = "/Users/aldendino/Documents/School/SitCalc/Alden/Documents/workspace/d28/original/domain-28.pddl"

with open(path) as file:
    text = file.read()
    domain = parsepddldomain(text)
    constructprolog(domain)

