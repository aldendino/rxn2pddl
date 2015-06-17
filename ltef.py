import argparse
import rxn
import pddl
import os.path

"""
These are the line by line specifications for the configuration file:
    The path to the directory holding the rxn files.
    The path to the text file containing a list of the rxn files to be run.
    The path to the directory for the domain file to be written.
    The filename for the directory.
    The path to the header file.
    The path to the footer file.
"""

def gen_pddl(args, reaction):
    #print str(reaction)
    pddl_domain = pddl.getDomain(reaction)
    print pddl_domain
    domain_file = os.path.join(args.output_dir,  "domain_" + reaction.name + ".pddl")
    with open(domain_file, 'w') as out:
        out.write(pddl_domain)
    print "PDDL domain description written to " + domain_file

# Create the argparser
# https://docs.python.org/dev/library/argparse.html

parser = argparse.ArgumentParser(description='Reads an RXN v3000 file and generates PDDL for the reaction.')
parser.add_argument('conf', type=str, help='The configuration file.')
args = parser.parse_args()

if not os.path.isfile(args.conf):
    raise IOError("Cannot open file " + args.conf)

with open(args.conf) as config:
    # Extract config file data
    (rxndir, rxnlist, domdir, domname, header, footer) = map((lambda x: x.rstrip("\n")), config)

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

with open(header) as head:
    with open(footer) as foot:
        domainstring = head.read() + "\n".join(actionlist) + foot.read()

with open(os.path.join(domdir, domname), "w") as domain_out:
    domain_out.write(domainstring)
