import argparse
import dist
import os.path

"""
usage: python conv.py configuration_file

These are the line by line specifications for the configuration file:
    The path to the directory holding the problem files.
    The path to the text file containing a list of the pddl problem files to be converted.
    The path to the directory where the converted files should be placed.
"""

parser = argparse.ArgumentParser(description='Convert pddl problem files to implement the distinct predicate.')
parser.add_argument('conf', type=str, help='The configuration file.')
args = parser.parse_args()

confpath = os.path.expanduser(args.conf)

if not os.path.isfile(confpath):
    raise IOError("Cannot open file " + confpath)

with open(confpath) as config:
    # Extract config file data
    (inputdir, inputlist, outputdir) = map(lambda x: x.rstrip("\n"), config)

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

with open(inputlist) as list:
    for line in list:
        filename = line.rstrip("\n")
        pddlfile = os.path.join(inputdir, filename)
        if not os.path.isfile(pddlfile):
            raise IOError("Cannot open file " + pddlfile)
        with open(pddlfile) as pddl:
            converted = dist.convertpddldistinct(pddl.read())
        pddlout = os.path.join(outputdir, filename)
        with open(pddlout, 'w') as out:
            out.write(converted)
        print "problem converted: %s" % pddlfile