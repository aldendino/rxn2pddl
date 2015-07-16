import commands
import sys
import os.path

# requires bash shell environment!
# New

# This script takes in a config file with a specific format
#   The path to the top level directory for fast-downward
#   The path to the domain file
#   The path to the problem files directory
#   The path to the text file which lists the problems to be run
#   The hueristic to be used
#   A line containing the string "new" or "old", specifying how to run fast-downward
#   The timeout value (see "man timeout" for options)
#   The path to the output directory

tee = "> >(tee %s) 2> >(tee %s >&2)"

def run_problem_new(filename, timeout):
    print(filename)
    output_file = os.path.join(out_path, filename)
    out = tee % (output_file + "-out.txt", output_file + "-err.txt")
    command = "timeout %s %sfast-downward.py %s %s%s --search %s %s" % \
              (timeout, fd_path, dm_path, pb_path, filename, heuristic, out)
    output = commands.getoutput(command)
    print(output)

def run_problem_old(filename, timeout):
    print(filename)
    output_file = os.path.join(out_path, filename)
    out = tee % (output_file + "-out.txt", output_file + "-err.txt")
    translate_command = "%stranslate/translate.py %s %s%s" % (fd_path, dm_path, pb_path, filename)
    preprocess_command = "%spreprocess/preprocess < output.sas" % (fd_path)
    search_command = "%ssearch/downward --search %s < output" % (fd_path, heuristic)
    command = "timeout %s %s && %s && %s %s" % \
              (timeout, translate_command, preprocess_command, search_command, out)
    output = commands.getoutput(command)
    print(output)

args = sys.argv[1:]

if len(args) != 1:
    raise Exception("usage: python " + sys.argv[0] + " config_file")

config_file = args[0]

with open(config_file) as config:
    (fd_path, dm_path, pb_path, ls_path, heuristic, opt_ver, timeout, out_path) = map((lambda line: line.rstrip("\n")), open(config_file))

    fd_path = os.path.expanduser(fd_path)
    dm_path = os.path.expanduser(dm_path)
    pb_path = os.path.expanduser(pb_path)
    ls_path = os.path.expanduser(ls_path)
    out_path = os.path.expanduser(out_path)

    print("fast-downard path:     " + fd_path)
    print("domain-path:           " + dm_path)
    print("problems path:         " + pb_path)
    print("problems list path:    " + ls_path)
    print("heuristic:             " + heuristic)
    print("fast-downward version: " + opt_ver)
    print("timeout:               " + timeout)
    print("Output path:           " + out_path)

    if opt_ver == "new":
        func = run_problem_new
    elif opt_ver == "old":
        func = run_problem_old
    else:
        raise Exception("version option must bve either \"new\" or \"old\"")

    for line in open(ls_path):
        filename = line.rstrip("\n")
        # Ignore blank lines
        if filename != "":
            func(filename, timeout)
