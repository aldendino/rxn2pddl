import commands
import sys

# This script takes in a config file with a specific format
#   The path to the top level directory for fast-downward
#   The path to the domain file
#   The path to the problem files directory
#   The path to the text file which lists the problems to be run
#   The hueristic to be used
#   A line containing the string "new" or "old", specifying how to run fast-downward

args = sys.argv[1:]

if len(args) != 1:
    raise Exception("usage: python " + sys.argv[0] + " config_file")

config_file = args[0]

(fd_path, dm_path, pb_path, ls_path, heuristic, opt_ver) = map((lambda line: line.rstrip("\n")), open(config_file))

print("fast-downard path:     " + fd_path)
print("domain-path:           " + dm_path)
print("problems path:         " + pb_path)
print("problems list path:    " + ls_path)
print("heuristic:             " + heuristic)
print("fast-downward version: " + opt_ver)

def run_problem_new(filename):
    print(filename)
    output_file = filename + ".txt"
    command = "timeout 2h %sfast-downward.py %s %s%s --search %s | tee %s" % (fd_path, dm_path, pb_path, filename, heuristic, output_file)
    output = commands.getoutput(command)
    print(output)

def run_problem_old(filename):
    print(filename)
    output_file = filename + ".txt"
    translate_command = "%stranslate/translate.py %s %s%s" % (fd_path, dm_path, pb_path, filename)
    preprocess_command = "%spreprocess/preprocess < output.sas" % (fd_path)
    search_command = "%ssearch/downward --search %s < output" % (fd_path, heuristic)
    command = "timeout 2h %s && %s && %s | tee %s" % (translate_command, preprocess_command, search_command, output_file)
    output = commands.getoutput(command)
    print(output)

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
        func(filename)
