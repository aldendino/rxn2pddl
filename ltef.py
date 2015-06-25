import argparse
import rxn
import pddl
import os.path

"""
usage: python ltef.py configuration_file

These are the line by line specifications for the configuration file:
    The path to the directory holding the rxn files.
    The path to the text file containing a list of the rxn files to be run.
    The path to the directory for the domain file to be written.
    The filename for the directory.
    The path to the header file.
    The path to the footer file.
"""

# Create the argparser
# https://docs.python.org/dev/library/argparse.html

parser = argparse.ArgumentParser(description='Reads RXN v3000 files and generates a PDDL domain for the reactions.')
parser.add_argument('conf', type=str, help='The configuration file.')
args = parser.parse_args()

confpath = os.path.expanduser(args.conf)

if not os.path.isfile(confpath):
    raise IOError("Cannot open file " + confpath)

with open(confpath) as config:
    # Extract config file data
    (rxndir, rxnlist, domdir, domname, header, footer) = map(lambda x: x.rstrip("\n"), config)

    # process for ~ symbol as home directory
    rxndir = os.path.expanduser(rxndir)
    rxnlist = os.path.expanduser(rxnlist)
    domdir = os.path.expanduser(domdir)

    # Check that everything that should exist does
    if not os.path.isdir(rxndir):
        raise IOError("Cannot open file " + rxndir)
    if not os.path.isfile(rxnlist):
        raise IOError("Cannot open file " + rxnlist)
    if not os.path.isdir(domdir):
        raise IOError("Cannot open file " + domdir)
    if not os.path.isfile(header):
        raise IOError("Cannot open file " + header)
    if not os.path.isfile(footer):
        raise IOError("Cannot open file " + footer)

# List of action strings
actionlist = []

with open(rxnlist) as list:
    for line in list:
        rxnfile = os.path.join(rxndir, line.rstrip("\n"))
        if not os.path.isfile(rxnfile):
            raise IOError("Cannot open file " + rxnfile)
        reaction = rxn.parse_rxn(rxnfile)
        pddl_domain = pddl.getDomain(reaction)
        actionlist.append(pddl_domain)
        print "reaction processed: %s" % rxnfile

with open(header) as head:
    with open(footer) as foot:
        domainstring = head.read() + "\n".join(actionlist) + foot.read()

domainpath = os.path.join(domdir, domname)
with open(domainpath, "w") as domain_out:
    domain_out.write(domainstring)
    print "domain written: %s" % domainpath
