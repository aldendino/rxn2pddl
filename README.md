# rxn2pddl
This is an rxn to pddl converter, based off of the project found at [https://github.com/vbatusov/ltef-chemistry]

This code has been tested to work on Python version 2.6.9, and requires the following libraries:
   
- argparse
- textfsm

Usage: `python ltef.py configuration_file`

##The configuration file is a text file with the following lines:

2. The path to the directory holding the rxn files.
3. The path to the text file containing a list of the rxn files to be run.
4. The path to the directory for the domain file to be written.
5. The filename for the directory.
6. The path to the header file.
7. The path to the footer file.
    
A sample configuration file "conf" is included with this project, meant to work with unix system directory structures.

Sample header, footer, and list files are included as well.

Make sure to modify the paths to work with your OS and directory structure.



