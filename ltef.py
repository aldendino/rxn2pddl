import argparse
import rxn
import pddl
import os.path


def gen_pddl(args, reaction):
    print str(reaction)
    pddl_domain = pddl.getDomain(reaction)
    print pddl_domain
    domain_file = os.path.join(args.output_dir,  "domain_" + reaction.name + ".pddl")
    out = open(domain_file, 'w')
    out.write(pddl_domain + "\n")
    out.close()
    print "\nPDDL domain description written to " + domain_file

# Create the argparser
# https://docs.python.org/dev/library/argparse.html

parser = argparse.ArgumentParser(description='Reads an RXN v3000 file and generates PDDL for the reaction.')

parser.add_argument('rxn_file',  type=str, help='The RXN v3000 file.')
parser.add_argument('output_dir', type=str, default='.', help='Output directory.')

args = parser.parse_args()

# Check if rxn file and output folder exist
if not os.path.isfile(args.rxn_file):
    raise IOError("Cannot open file " + args.rxn_file)

if not os.path.isdir(args.output_dir):
    raise IOError("Cannot open directory " + args.rxn_file)

# Parse the RXN file, get a generic reaction
reaction = rxn.parse_rxn(args.rxn_file)

gen_pddl(args, reaction)
