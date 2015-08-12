import re

"""
Grammar:

    start = pddl
    pddl = space "(" space contents space ")" space
    contents = space define space objects space init space goal space
    define = "define" space "(problem" space problem ")" space "(:domain" domain ")"
    objects = "(:objects" space (space (object|comment) space)* ")"
    object = id space "-" space type
    id = word
    type = word
    init = "(:init" space initcontent ")"
    goal = "(:goal" space goalcontent ")"
    initcontent = ?
    goalcontent = ?
    problem = word
    domain = word
    word = w+
    space = (" "|\t|\n)*
    comment = ";" (space | word)* "\n"
"""

""" Remove from the front of a string any of the characters in a list """
def removeleadingchars(input, charlist):
    while (len(input) > 0) and (input[0] in charlist):
        input = input[1:]
    return input


""" Remove from the end of a string any of the characters in a list """
def removetrailing(input, charlist):
    while input[len(input)-1] in charlist:
        input = input[:len(input)-1]
    return input


""" Remove a specified string from the front of the list, and raise an exception if it is not there """
def removeleadingstring(input, string):
    if input.startswith(string):
        return input.lstrip(string)
    else:
        raise Exception("missing: " + string)


""" Separate a string into a tuple based on the first occurrence of a delimiter """
def readuntilchar(input, char):
    count = 0
    while input[count] != char:
        count += 1
    content = input[0:count]
    leftover = input[count:]
    return content, leftover


""" Separate a string into a tuple based on the first occurrence of a delimiter """
def readuntilchars(input, charlist):
    count = 0
    while input[count] not in charlist:
        count += 1
    content = input[0:count]
    leftover = input[count:]
    return content, leftover


"""
    Sepatate a string into a header, extraction, and footer, based on a start and end delimiter
    Note that this preserves the structure of nested occurrences of the specified delimiters
"""
def extractsection(input, startdelim, enddelim):
    extraction = ""
    start = 0
    end = 0
    startdelimcount = 0
    enddelimcount = 0
    for i in range(0, len(input)):
        if input[i] == startdelim:
            startdelimcount += 1
            if startdelimcount == 1:
                start = i + 1
        elif input[i] == enddelim:
            enddelimcount += 1
        if (startdelimcount == enddelimcount) and (startdelimcount != 0):
            end = i
            header = input[0:start-1]
            extraction = input[start:end]
            footer = input[end+1:len(input)]
            return (header, extraction, footer)


""" Parse the objects as a list of id and type tuples """
def parseobjects(objects, ignorelist):
    objectslist = []

    #itemlist = re.split(r' |\n|\t', objects)
    #while len(itemlist) >= 3:
    #    paramid = itemlist[0]
    #    dash = itemlist[1]
    #    paramtype = itemlist[2]
    #    itemlist = itemlist[3:]
    #    objectslist.append((paramid, paramtype))

    for line in objects.rsplit("\n"):
        line = removeleadingchars(line, ignorelist)
        if line == "":
            continue
        if line[0] == ";":
            continue
        itemlist = re.split(r' |\n|\t', line)
        if len(itemlist) >= 3:
            paramid = itemlist[0]
            dash = itemlist[1]
            paramtype = itemlist[2]
            if dash != "-":
                continue
            objectslist.append((paramid, paramtype))

    return objectslist

""" Parse the init section """
def parseinit(pddl):
    pass


""" Parse the goal section """
def parsegoal(pddl):
    pass


""" Parse a pddl string and extract the data as a tuple """
def parse(pddl):
    ignorelist = [' ', '\n', '\t']

    problemname = ""
    domainname = ""
    objectlist = []
    initcontent = ""
    goalcontent = ""

    (_, content, _) = extractsection(pddl, '(', ')')
    (define, problem, content) = extractsection(content, '(', ')')
    (_, domain, content) = extractsection(content, '(', ')')
    (_, objects, content) = extractsection(content, '(', ')')
    (_, init, content) = extractsection(content, '(', ')')
    (_, goal, content) = extractsection(content, '(', ')')

    define = removeleadingchars(define, ignorelist)
    removeleadingstring(define, "define")

    problem = removeleadingchars(problem, ignorelist)
    problem = removeleadingstring(problem, "problem")
    problem = removeleadingchars(problem, ignorelist)
    problemname = problem

    domain = removeleadingchars(domain, ignorelist)
    domain = removeleadingstring(domain, ":domain")
    domain = removeleadingchars(domain, ignorelist)
    domainname = domain

    objects = removeleadingchars(objects, ignorelist)
    objects = removeleadingstring(objects, ":objects")
    objects = removeleadingchars(objects, ignorelist)
    objectlist = parseobjects(objects, ignorelist)

    init = removeleadingchars(init, ignorelist)
    init = removeleadingstring(init, ":init")
    init = removeleadingchars(init, ignorelist)
    initcontent = init

    goal = removeleadingchars(goal, ignorelist)
    goal = removeleadingstring(goal, ":goal")
    goal = removeleadingchars(goal, ignorelist)
    goalcontent = goal

    return problemname, domainname, objectlist, initcontent, goalcontent


"""
    Reconstruct the pddl string from a tuple with the addition of
    bidirectional pairwise distinct predicates over the objects in the init section
"""
def reconstructpddlwithdistinct((problemname, domainname, objectlist, initcontent, goalcontent)):
    problem = "(problem %s)" % problemname
    domain = "(:domain %s)" % domainname

    objects = "(:objects\n"
    for (id, type) in objectlist:
        objects += "%s - %s\n" % (id, type)
    objects += ")"

    distinct = ""
    for (id1, _) in objectlist:
        for (id2, _) in objectlist:
            if id1 != id2:
                distinct += "(distinct %s %s)\n" % (id1, id2)
    initcontent = distinct + initcontent

    init = "(:init\n%s)" % initcontent
    goal = "(:goal\n%s)" % goalcontent

    contents = "%s\n%s\n%s\n%s\n%s\n" % (problem, domain, objects, init, goal)

    return "(define\n%s)" % contents


""" Sanitizes the comments, since they can include parenthisis, which will mess up the extract function """
def sanitizecomments(pddl):
    sanitized = ""
    for line in pddl.split("\n"):
        line = removeleadingchars(line, [' ', '\t'])
        if not line.startswith(";"):
            sanitized += line + "\n"
    return sanitized


""" Analyze properies about the number of objects in total and of specific types """
def analyzeobjects(objectlist):
    objectdict = {}
    for (id, type) in objectlist:
        if type in objectdict:
            objectdict[type] += 1
        else:
            objectdict[type] = 1
    for key in objectdict.keys():
        print "type: %s * %s" % (key, objectdict[key])
    print "total objects: %s" % len(objectlist)


""" Convert a pddl problem string to have distinct bidirectional pairwise predicates in the init section """
def convertpddldistinct(pddl):
    sanitizedpddl = sanitizecomments(pddl)
    parsed = parse(sanitizedpddl)
    analyzeobjects(parsed[2])
    return reconstructpddlwithdistinct(parsed)


#with open(file) as pddlfile:
#    pddl = pddlfile.read()
#    out = parse(pddl)
#    print reconstructpddlwithdistinct(out)

#print extractsection("how   do(hello (you guys))what     foo", '(', ')')