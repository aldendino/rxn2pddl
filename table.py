import csv
import re
import os.path
import argparse

"""
usage: python table.py configuration_file

These are the line by line specifications for the configuration file:
    The path to the directory holding the results files.
    The path to the text file containing a list of the results files to be used.
    The path to the directory where the generated files should be placed.
    The name of the cvs file (without extension).
"""

class Results:
    categorylist = ["Problem", "Solution", "Total Time (s)", "Peak Memory (KB)", "Plan Cost", "Variables",
                    "Facts", "Bytes per State", "Relevant Atoms", "Auxiliary Atoms"]

    def __init__(self, solution, totaltime, peakmemory, plancost, variables, facts,
                 bytesperstate, relevantatoms, auxiliaryatoms):
        self.sol = solution
        self.tottime = totaltime
        self.peakmem = peakmemory
        self.plancost = plancost
        self.vars = variables
        self.facts = facts
        self.bps = bytesperstate
        self.relatoms = relevantatoms
        self.auxatoms = auxiliaryatoms

    def aslist(self):
        return [self.sol, self.tottime, self.peakmem, self.plancost, self.vars,
                self.facts, self.bps, self.relatoms, self.auxatoms]


def resolvesearch(search):
    result = "-"
    if search is not None:
        result = search.group(1)
    return result


def parseresults(resultstring):
    sol = ""
    tottime = resolvesearch(re.search(r'Total time: ([\d.]+)s', resultstring))
    peakmem = resolvesearch(re.search(r'Peak memory: ([\d.]+) KB', resultstring))
    plancost = resolvesearch(re.search(r'Plan cost: ([\d]+)', resultstring))
    vars = resolvesearch(re.search(r'Variables: ([\d]+)', resultstring))
    facts = resolvesearch(re.search(r'Facts: ([\d]+)', resultstring))
    bps = resolvesearch(re.search(r'Bytes per state: ([\d]+)', resultstring))
    relatoms = resolvesearch(re.search(r'([\d]+) relevant atoms', resultstring))
    auxatoms = resolvesearch(re.search(r'([\d]+) auxiliary atoms', resultstring))
    return Results(sol, tottime, peakmem, plancost, vars, facts, bps, relatoms, auxatoms)


def writecsv(filename, iterable):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(iterable)


parser = argparse.ArgumentParser(description='Generate a results csv file')
parser.add_argument('conf', type=str, help='The configuration file.')
args = parser.parse_args()

confpath = os.path.expanduser(args.conf)

if not os.path.isfile(confpath):
    raise IOError("Cannot open file " + confpath)

with open(confpath) as config:
    # Extract config file data
    (inputdir, inputlist, outputdir, outputfile) = map(lambda x: x.rstrip("\n"), config)

    # process for ~ symbol as home directory
    inputdir = os.path.expanduser(inputdir)
    inputlist = os.path.expanduser(inputlist)
    outputdir = os.path.expanduser(outputdir)

    # Check that everything that should exist does
    if not os.path.isdir(inputdir):
        raise IOError("Cannot open file " + inputdir)
    if not os.path.isfile(inputlist):
        raise IOError("Cannot open file " + inputlist)
    if not os.path.isdir(outputdir):
        raise IOError("Cannot open file " + outputdir)

outputpath = os.path.join(outputdir, outputfile)

with open(inputlist, 'r') as list:
    with open(outputfile, 'wb') as f:
        outputlist = []
        outputlist.append(Results.categorylist)
        for line in list:
            filename = line.rstrip("\n")
            #print filename
            filepath = os.path.join(inputdir, filename)
            problemname = os.path.splitext(filename)[0]
            with open(filepath, 'r') as fp:
                result = [problemname] + parseresults(fp.read()).aslist()
                outputlist.append(result)
                #print result
            print "%s processed" % filename
        writecsv(outputpath, outputlist)




#with open(file, 'r') as f:
#    problem = os.path.splitext(os.path.basename(file))[0]
#    list = [[problem] + parseresults(f.read()).aslist()]
#    print list
#    writecsv('/Users/aldendino/Desktop/test.csv', list)
