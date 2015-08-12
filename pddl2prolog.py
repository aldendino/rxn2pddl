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
        prec += "poss(" + action.actionname + constructparameters(action.paramlist, 'S') + " :- " \
                + constructaxioms((posprecaxioms, negprecaxioms), action.paramdict) + "\n"
    return prec


def constructposeffects(action):
    poseffaxioms, negeffaxioms = action.efflist
    poseffstr = ""
    for poseff in poseffaxioms:
        poseffparams = map(lambda paramid: (paramid, action.paramdict[paramid]), poseff[1])
        poseffstr += poseff[0] + constructparameters(poseffparams, '[A|S]') + " :- A = " \
               + action.actionname + constructparameters(action.paramlist, 'S') + ".\n"
    return poseffstr


def constructprolog(parseddomain):
    preclist = []
    efflist = []

    negeff = ""
    negeffdict = {}
    for action in parseddomain.actions:
        preclist.append(constructpreconditions(action))
        efflist.append(constructposeffects(action))

        # negative effect collector... how should different parameter names be handled?
        poseffaxioms, negeffaxioms = action.efflist
        for negeff in negeffaxioms:
            if negeff[0] in negeffdict:
                negeffdict[negeff[0]].append(action.actionname)
            else:
                negeffdict[negeff[0]] = [action.actionname]

    print negeffdict

    for negeffkey in negeffdict:
        print negeffkey + " :- " + str(negeffdict[negeffkey])

    precstr = ""
    for item in preclist: precstr += item

    effstr = ""
    for item in efflist: effstr += item

    #print precstr
    #print effstr


path = "/Users/aldendino/Documents/School/SitCalc/Alden/Documents/Res/AIPS-2000DataFiles/2000-Tests/Blocks/Track1/Typed/domain.pddl"

with open(path) as file:
    text = file.read()
    domain = parsepddldomain(text)
    constructprolog(domain)




































#def sanitizechars(text, list):
#    sanitized = ""
#    for i in range(0, len(text)):
#        if text[i] not in list:
#            sanitized += text[i]
#    return sanitized
#
#
#
#def section(text, startdelim, enddelim):
#
#    startpos = 0
#
#    startcount = 0
#    endcount = 0
#
#    for i in range(0, len(text)):
#        if text[i] == startdelim:
#            startcount += 1
#            if startcount == 1:
#                startpos = i
#        if text[i] == enddelim:
#            endcount += 1
#        if startcount == endcount and startcount != 0:
#            head = text[0:startpos]
#            body = section(text[startpos+1:i], startdelim, enddelim)
#            tail = section(text[i+1:len(text)], startdelim, enddelim)
#            info = [head, body, tail]
#            info = filter(None, info)
#            return info
#
#    return None
#
##print section("hello (my (darling)) world", '(', ')')
#
#path = "/Users/aldendino/Documents/School/SitCalc/Alden/Documents/Res/AIPS-2000DataFiles/2000-Tests/Blocks/Track1/Typed/domain.pddl"
#
#
#def printinfo(info):
#    for i in info:
#        if type(i) == type(list):
#            printinfo(i)
#        else:
#            print i
#
#with open(path) as file:
#    text = file.read()
#    santext = sanitizechars(text, ['\n', '\t'])
#    printinfo(section(santext, '(', ')'))