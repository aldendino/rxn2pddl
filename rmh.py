import sexpdata
import argparse


class Problem:
    def __init__(self):
        self.name = ""
        self.domain = ""
        self.objects = {}
        self.init = []
        self.goal = []


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


def checkpddl(pddl):
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
    templist = []
    typeflag = False
    for item in objects:
        if typeflag:
            objectdict[item] = templist
            templist = []
            typeflag = False
        else:
            if item == "-":
                typeflag = True
            else:
                templist.append(item)
    return objectdict


def parseinit(init):
    return map(lambda item: (item[0], item[1:]), init)


def parsegoal(goal):
    return map(lambda item: (item[0], item[1:]), goal[0][1:])


def parseproblem(pddl):
    checkpddl(pddl)

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
                print parameter
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



def rmhfromdomain(pddl):
    pass


parser = argparse.ArgumentParser(description='Remove unnecessary hydrogens from pddl problems.')
parser.add_argument('problem', type=str, help='The input path to a pddl problem file.')
args = parser.parse_args()

with open(args.problem, 'r') as file:
    pddl = file.read()
    rmhfromproblem(pddl)