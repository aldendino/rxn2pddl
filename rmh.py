import sexpdata
import argparse


class Problem:
    def __init__(self):
        self.name = ""
        self.domain = ""
        self.objects = {}
        self.init = []
        self.goal = []


class Domain:
    def __init__(self):
        self.name = ""
        self.requirements = []
        self.types = {}
        self.predicates = []
        self.actions = []


def stripsexp(sexp):
    if isinstance(sexp, sexpdata.Symbol):
        return sexp._val
    elif isinstance(sexp, list):
        return map(stripsexp, sexp)
    else:
        return sexp


def importpddl(pddl):
    data = sexpdata.loads(pddl)
    stripeddata = stripsexp(data)
    return stripeddata


def checkproblem(pddl):
    if pddl[0] != "define":
        raise IOError("Missing definition.")
    if pddl[1][0] != "problem":
        raise IOError("Missing problem")
    if pddl[2][0] != ":domain":
        raise IOError("Missing domain")
    if pddl[3][0] != ":objects":
        raise IOError("Missing objects")
    if pddl[4][0] != ":init":
        raise IOError("Missing init")
    if pddl[5][0] != ":goal":
        raise IOError("Missing goal")


def parseobjects(objects):
    objectdict = {}
    typeflag = False
    tempitem = ""
    for item in objects:
        if typeflag:
            if item in objectdict:
                objectdict[item].append(tempitem)
            else:
                objectdict[item] = [tempitem]
            typeflag = False
        elif item == "-":
            typeflag = True
        else:
            tempitem = item
    return objectdict


def parseinit(init):
    return map(lambda item: (item[0], item[1:]), init)


def parsegoal(goal):
    return map(lambda item: (item[0], item[1:]), goal[0][1:])


def parseproblem(pddl):
    checkproblem(pddl)

    problem = Problem()
    problem.name = pddl[1][1]
    problem.domain = pddl[2][1]
    problem.objects = parseobjects(pddl[3][1:])
    problem.init = parseinit(pddl[4][1:])
    problem.goal = parsegoal(pddl[5][1:])

    return problem


def filterbonds(problem, inlist, outlist, hset):
    hydrogens = problem.objects["hydrogen"]
    carbons = problem.objects["carbon"]

    for fluent in inlist:
        parameters = fluent[1]
        # ignore if the fluent if obviously not a bond
        if len(parameters) != 2:
            outlist.append(fluent)
        else:
            hc = (parameters[0] in hydrogens) and (parameters[1] in carbons)
            ch = (parameters[1] in hydrogens) and (parameters[0] in carbons)
            if not hc and not ch:
                outlist.append(fluent)
                if parameters[0] in hydrogens:
                    hset.add(parameters[0])
                if parameters[1] in hydrogens:
                    hset.add(parameters[1])


def filterhset(hset, *fluentlists):
    for fluentlist in fluentlists:
        for fluent in fluentlist:
            for parameter in fluent[1]:
                #print parameter
                if parameter in hset:
                    hset.remove(parameter)


def rmhfromproblem(pddl):
    problem = parseproblem(importpddl(pddl))

    rmh = Problem()
    rmh.name = problem.name
    rmh.domain = problem.domain

    initlist = []
    goallist = []
    hset = set()

    filterbonds(problem, problem.init, initlist, hset)
    filterbonds(problem, problem.goal, goallist, hset)

    filterhset(hset, initlist, goallist)
    print hset

    # hset is empty once filtered, so how can we remove any items?

    rmh.objects = problem.objects # should filter out hydrogen objects first
    rmh.init = initlist
    rmh.goal = goallist

    return rmh


def constructfluentstrings(fluentlist):
    return map(lambda (name, params): "{0}({1})".format(name, ", ".join(params)), fluentlist)


def constructobjectstrings(objectdict):
    return map(lambda key: "\n\t".join(map(lambda item: "{0} - {1}".format(item, key), objectdict[key])), objectdict)


def constructproblem(problem):
    #"(define\n\t(problem {0})\n\t(:domain {1}))".format(problem.name, problem.domain)

    name = "\t(problem {0})".format(problem.name)
    domain = "\t(:domain {0})".format(problem.domain)
    objects = "(:objects\n\t{0})".format("\n\t".join(constructobjectstrings(problem.objects)))
    init = "(:init\n\t{0})".format("\n\t".join(constructfluentstrings(problem.init)))
    goal = "(:goal\n\t(and\n\t\t{0}))".format("\n\t\t".join(constructfluentstrings(problem.goal)))

    body = "\n".join([name, domain, objects, init, goal])
    final = "(define\n{0})".format(body)
    return final


def parsedomain(pddl):
    pass


def rmhfromdomain(pddl):
    domain = parsedomain(importpddl(pddl))


parser = argparse.ArgumentParser(description='Remove unnecessary hydrogens from pddl problems.')
parser.add_argument('problem', type=str, help='The input path to a pddl problem file.')
args = parser.parse_args()

with open(args.problem, 'r') as file:
    pddl = file.read()
    print constructproblem(rmhfromproblem(pddl))