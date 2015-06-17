import copy
import random
import re


class Atom:
    """This class is geared to store atom information supplied by v3000 molfiles"""

    def __init__(self, symbol, x, y, z, rxnIndex, rxnAAM, attribs={}, aam=0):
        self.symbol = symbol
        self.aam = aam # This a working, sanitized AAM, doesn't have to be the same as rxnAAM
        self.x = x
        self.y = y
        self.z = z
        self.rxnIndex = rxnIndex
        self.rxnAAM = rxnAAM
        self.attribs = attribs
        self.mass = 0
        self.charge = 0

    def __str__(self):
        return "<Atom " + self.symbol + " at (" + ", ".join([str(self.x), str(self.y), str(self.z)]) + ") with AAM=" + str(self.aam) + " (old rxn " + str(self.rxnAAM) + ") and attribs " + str(self.attribs) + " />"

    def __eq__(self, other):
        return type(self) == type(other) and self.symbol == other.symbol and self.aam == other.aam


class Bond:
    """v3000 bond information container"""

    'fromAtom and toAtom must be Atom objects!'
    def __init__(self, rxnIndex, order, fromAtom, toAtom, attribs={}):
        self.rxnIndex = rxnIndex
        self.order = order
        self.fromAtom = fromAtom
        self.toAtom = toAtom
        self.attribs = attribs

    def __str__(self):
        return "<Bond with order " + str(self.order) + " between AAM " + str(self.fromAtom.aam) + " and " + str(self.toAtom.aam) + " />"

    def __eq__(self, other):
        #print "(comparing bonds)"
        #print "  self: " + str(self)
        #print "  other: " + str(other)
        
        return type(self) == type(other) and self.order == other.order and ((self.fromAtom == other.fromAtom and self.toAtom == other.toAtom) or (self.fromAtom == other.toAtom and self.toAtom == other.fromAtom))


class Molecule:
    """ A molecule can be either a complete molecule or a fragment.
    The difference is in the self.anchor: it is the attachment point
    which for a fragment is a pointer to one of its atoms and for a
    complete molecule is None.

    A molecule may contain pseudoatoms ("Alkyl") and R-group atoms ("R1").
    """

    def __init__(self):
        self.atomList = []
        self.bondList = []
        self.anchor = None

    def addAtom(self, *atom):
        for a in atom:
            #print "Adding atom " + str(a)
            self.atomList.append(a)

    def addBond(self, bond):
        self.bondList.append(bond)

    def __str__(self):
        desc = "<Molecule>"
        for atom in self.atomList:
            desc += "\n  " + str(atom)
        for bond in self.bondList:
            desc += "\n  " + str(bond)
        desc += "\n</Molecule>"
        return desc

    def inferAtomsFromBonds(self):
        """
        discards self.atomList, replaces it with an array of atoms gathered from bonds
        """
        self.atomList = []
        #print "Recomputing atoms"
        for b in self.bondList:
            if b.toAtom not in self.atomList:
                self.atomList.append(b.toAtom)
                #print "Adding atom with aam " + str(b.toAtom.aam)
            if b.fromAtom not in self.atomList:
                self.atomList.append(b.fromAtom)
                #print "Adding atom with aam " + str(b.fromAtom.aam)
    def isDiatomicHalogen(self):
        if (len(self.bondList) == 1 and len(self.atomList) == 2 and 
                self.atomList[0].symbol == "X" and self.atomList[1].symbol == "X"):
            #print "This molecule is a diatomic halogen: " + str(self)
            return True
        return False

    @property
    def numberOfAtoms(self):
        return len(self.atomList)

    def replaceAtomWithMolecule(self, oldatom, newmolecule):
        """ Used by Molecule.getInstance, this method alters 'self' by replacing a given atom
        object with another one in atomList, and then correcting the bonds to point to the
        new atom. Finally, the remaining atoms and bonds in given molecule are added to 'self'.
        """

        if newmolecule.anchor is None:
            raise Exception("New molecule does not have an anchor!")

        newmolecule.anchor.aam = oldatom.aam

        # Correct the bonds to anchor of new molecule
        for bond in self.bondList:
            if bond.toAtom is oldatom:
                bond.toAtom = newmolecule.anchor
            if bond.fromAtom is oldatom:
                bond.fromAtom = newmolecule.anchor

        # Add remaining atoms and bonds to current molecule
        self.atomList = filter(lambda a: a is not oldatom, self.atomList)
        self.atomList.extend(newmolecule.atomList)  # Is extend shallow or deep? Assume shallow.
        self.bondList.extend(newmolecule.bondList)


        # FINISHED, UNTESTED


    def getInstance(self, rgroups={}):
        """ This returns a new molecule which is the same as self except that every
        R-atom is replaced with a corresponding molecule from the provided dictionary.
        """
        # This will be returned
        newmol = copy.deepcopy(self)

        #print "Molecule instantiation in progress..."
        #print "New copy of original:\n" + str(newmol)

        # In the copy, replace each occurence of an R-atom with an actual R-instance
        for atom in newmol.atomList:
            #print "Looking at atom " + atom.symbol
            if atom.symbol in rgroups.keys():
                #print "An R-group is found! Replacing it with a sub-molecule..."
                newmol.replaceAtomWithMolecule(atom, rgroups[atom.symbol])

        #print "molecule.getInstance: ORIGINAL\n" + str(self)
        #print "molecule.getInstance: RESULT\n" + str(newmol)
            
        return newmol

        # FINISHED, UNTESTED


class Reaction:
    """stores a set of reactants, agents, products, and rgroups

    rgroups is a dictionary "R1" : [R-molecule, R-molecule, ...]
    """

    def __init__(self, name="unknown_reaction", full_name="Unknown Reaction", desc="No description"):
        self.desc = desc    # reaction description from text file
        self.name = name    # basename (unique identifier), also used as reaction name in PDDL
        self.full_name = full_name  # Official human-readable name from YAML file
        self.params = {}    # for instantiation parameters; generic reaction params are {}
        self.reactants = []
        self.agents = []
        self.products = []
        self.rgroups = {}


    def __str__(self):
        desc = "<Reaction>"
        desc += "\n  <Reactants>"
        for r in self.reactants:
            desc += "\n    " + ('\n    ').join(str(r).split('\n'))
        desc += "\n  </Reactants>\n  <Agents>"
        for a in self.agents:
            desc += "\n    " + ('\n    ').join(str(a).split('\n'))
        desc += "\n  </Agents>\n  <Products>"
        for p in self.products:
            desc += "\n    " + ('\n    ').join(str(p).split('\n'))
        desc += "\n  </Products>\n  <R-groups>"
        for g in self.rgroups.keys():
            desc += "\n    <R-group No. " + g + ">"
            for g2 in self.rgroups[g]:
                desc += "\n      " + ('\n      ').join(str(g2).split('\n'))
            desc += "\n    </R-group No. " + g + ">"
        desc += "\n  </R-groups>\n<Reaction>"

        return desc

    @property
    def numberOfAtomsInReactants(self):
        """ Counts all atoms (including pseudoatoms and R-atoms) in reactants."""
        num = 0

        for mol in self.reactants:
            num += mol.numberOfAtoms

        return num

    @property
    def numberOfAtomsOverall(self):
        """ Counts all atoms (including pseudo and R) in reaction, including catalysts."""
        num = self.numberOfAtomsInReactants

        for mol in self.agents:
            num += mol.numberOfAtoms

        return num

    def addReactant(self, molecule):
        self.reactants.append(molecule)

    def addAgent(self, molecule):
        self.agents.append(molecule)

    def addProduct(self, molecule):
        self.products.append(molecule)

    def addRGroup(self, rgroupNumber, molecule):
        rgroupName = "R" + str(rgroupNumber)
        if rgroupName not in self.rgroups:
            self.rgroups[rgroupName] = []
        self.rgroups[rgroupName].append(molecule)

    def finalize(self):
        """Merely a sanity check
        Only execute after everything has been added to reaction."""

        aamReactants = []
        aamAgents = []
        aamProducts = []

        for mol in self.reactants:
            for atom in mol.atomList:
                #print "Sanity: " + str(atom)
                if atom.aam == 0:
                    raise Exception("Sanity check: reaction contains a reactant atom with AAM = 0")
                if atom.aam in aamReactants:
                    raise Exception("Sanity check: reaction contains two reactant atoms with the same AAM, #" + str(atom.aam) + ";\n current atom: " + str(atom))
                else:
                    aamReactants.append(atom.aam)

        for mol in self.agents:
            for atom in mol.atomList:
                if atom.aam == 0:
                    raise Exception("Sanity check: reaction contains a catalyst atom with AAM = 0")
                if atom.aam in aamAgents:
                    raise Exception("Sanity check: reaction contains two catalyst atoms with the same AAM, #" + str(atom.aam) + ";\n current atom: " + str(atom))
                else:
                    aamAgents.append(atom.aam)

        for mol in self.products:
            for atom in mol.atomList:
                if atom.aam == 0:
                    raise Exception("Sanity check: reaction contains a product atom with AAM = 0")
                if atom.aam in aamProducts:
                    raise Exception("Sanity check: reaction contains two product atoms with the same AAM, #" + str(atom.aam) + ";\n current atom: " + str(atom))
                else:
                    aamProducts.append(atom.aam)

        if len(set(aamReactants).intersection(set(aamProducts))) != len(aamReactants):
            print "Reaction: " + str(self.name)
            print "Reactants: " + str(aamReactants)
            print "Products: " + str(aamProducts)

            print "Reactants: " + str([str(r) for r in self.reactants])
            print "Products: " + str([str(r) for r in self.products])
            raise Exception("Sanity check: mismatch between reactant and product atom sets")

        if len(set(aamReactants).intersection(set(aamAgents))) != 0:
            raise Exception("Sanity check: reactants and catalyst share some atoms")

        if self.numberOfAtomsOverall != len(aamReactants + aamAgents):
            raise Exception("Sanity check: self.numberOfAtomsOverall != len(aamReactants + aamAgents)")


def sanitize_name(name):
    return re.sub(r'\W+', '', name).lower()


def sanitize_symbol(name):
    return re.sub(r'[^a-zA-Z0-9_-]+', '', name).lower()


def pseudoatomToList(string):
    #print "Unwrapping a symbol list " + string
    if string[0] == "[" and string[-1] == "]":
        #print "  success"
        return re.findall('(?:([a-zA-Z0-9-]+),?)', string[1:-1])
    else:
        #print "  failure"
        return [string]


def getInstanceByName(atom): 
    """ 
        This method returns an actual instance of a pseudoatom.
    """
    #print "Getting instance of " + sanitize_symbol(atom.symbol)
    anchor_aam = atom.aam
    standard_name = sanitize_symbol(atom.symbol)
    build_function = PSEUDO[standard_name][0]
    args = PSEUDO[standard_name][1]

    return build_function(anchor_aam, args)


def buildAlkyl(anchorAAM, args):
    """ Must return a molecule whose anchor is not None """

    # args["size"] is a list of integers
    # must select a size arbitrarily from list
    size = int(random.choice(args["size"]))

    if size < 1:
        raise Exception("Alkyl size cannot be less than one!")

    molecule = Molecule()
    root = Atom("C", 0, 0, 0, 0, 0)
    root.aam = anchorAAM
    molecule.addAtom(root)
    molecule.anchor = root

    if size == 100: # special case
        
        # Starting atom of the ring
        c1 = None

        # gamble on whether it's a phenyl or a benzyl
        if random.randint(0,1) == 0:
            # saturate root with hydrogens
            h1 = Atom("H", 0, 0, 0, 0, 0)
            h2 = Atom("H", 0, 0, 0, 0, 0)
            molecule.addAtom(h1, h2)
            molecule.addBond(Bond(0, 1, root, h1))
            molecule.addBond(Bond(0, 1, root, h2))
            # create a new atom as the ring starter
            c1 = Atom("C", 0, 0, 0, 0, 0)
            molecule.addAtom(c1)
            molecule.addBond(Bond(0, 1, root, c1))
        else:
            # otherwise, ring includes the root
            c1 = root

        # build a ring
        
        c2 = Atom("C", 0, 0, 0, 0, 0)
        c3 = Atom("C", 0, 0, 0, 0, 0)
        c4 = Atom("C", 0, 0, 0, 0, 0)
        c5 = Atom("C", 0, 0, 0, 0, 0)
        c6 = Atom("C", 0, 0, 0, 0, 0)
        molecule.addAtom(c2, c3, c4, c5, c6)
        molecule.addBond(Bond(0, 1, c1, c2))
        molecule.addBond(Bond(0, 2, c2, c3))
        molecule.addBond(Bond(0, 1, c3, c4))
        molecule.addBond(Bond(0, 2, c4, c5))
        molecule.addBond(Bond(0, 1, c5, c6))
        molecule.addBond(Bond(0, 2, c6, c1))

    else:   # arbitrary tree without rings

        (size1, size2, size3) = splitThreeWays(size - 1)
        
        buildAlkylTree(molecule, root, size1)
        buildAlkylTree(molecule, root, size2)
        buildAlkylTree(molecule, root, size3)

    return molecule


def buildAlkylTree(molecule, anchor, size) :
    if size < 1 :
        atom = Atom("H", 0, 0, 0, 0, 0)

        molecule.addAtom(atom)
        if anchor is not None:
            molecule.addBond(Bond(0, 1, anchor, atom))
    else : # assume size is non-negative
        # create new carbon
        atom = Atom("C", 0, 0, 0, 0, 0)

        molecule.addAtom(atom)
        # link it back to parent
        if anchor is not None:
            molecule.addBond(Bond(0, 1, anchor, atom))

        (size1, size2, size3) = splitThreeWays(size - 1)
        
        buildAlkylTree(molecule, atom, size1)
        buildAlkylTree(molecule, atom, size2)
        buildAlkylTree(molecule, atom, size3)


def splitThreeWays(number):
    a = random.random()
    b = random.random()
    c = random.random()
    whole = a + b + c
    coeff = number / whole
    resA = int(round(coeff * a))
    resB = int(round(coeff * b))
    resC = int(number - resA - resB)
    #print "Splitting " + str(number) + " yields " + str((resA,resB,resC))
    return (resA,resB,resC)


def buildHalogen(anchorAAM, args):
    #print "Invoked buildHalogen with args = " + str(args)
    symbol = random.choice(args["symbol"])

    molecule = Molecule()
    root = Atom(symbol, 0, 0, 0, 0, 0)
    root.aam = anchorAAM
    molecule.addAtom(root)
    molecule.anchor = root

    return molecule


def buildLindlarsCatalyst(anchorAAM, args):
    molecule = Molecule()
    root = Atom("Lindlar's catalyst", 0, 0, 0, 0, 0)
    root.aam = anchorAAM
    molecule.addAtom(root)
    molecule.anchor = root

    return molecule


def buildTosylate(anchorAAM, args):
    molecule = Molecule()
    root = Atom("Ts", 0, 0, 0, 0, 0)
    root.aam = anchorAAM
    molecule.addAtom(root)
    molecule.anchor = root
    oxygen = Atom("O", 0, 0, 0, 0, 0, {"CHG" : "-1"})
    molecule.addAtom(oxygen)
    molecule.addBond(Bond(0, 1, root, oxygen))

    return molecule


def buildBromineAnion(anchorAAM, args):
    molecule = Molecule()
    root = Atom("Br", 0, 0, 0, 0, 0, {"CHG" : "-1"})
    root.aam = anchorAAM
    molecule.addAtom(root)
    molecule.anchor = root

    return molecule

def buildIodineAnion(anchorAAM, args):
    molecule = Molecule()
    root = Atom("I", 0, 0, 0, 0, 0, {"CHG" : "-1"})
    root.aam = anchorAAM
    molecule.addAtom(root)
    molecule.anchor = root

    return molecule


def buildROH(anchorAAM, args):
    molecule = Molecule()
    root = Atom("smthng", 0, 0, 0, 0, 0)
    root.aam = anchorAAM
    molecule.addAtom(root)
    molecule.anchor = root
    oxygen = Atom("O", 0, 0, 0, 0, 0)
    hydrogen = Atom("H", 0, 0, 0, 0, 0)
    molecule.addAtom(oxygen)
    molecule.addAtom(hydrogen)
    molecule.addBond(Bond(0, 1, root, oxygen))
    molecule.addBond(Bond(0, 1, hydrogen, oxygen))
    return molecule


def buildAmmonia(anchorAAM, args):
    molecule = Molecule()
    root = Atom("N", 0, 0, 0, 0, 0)
    root.aam = anchorAAM
    molecule.addAtom(root)
    molecule.anchor = root
    h1 = Atom("H", 0, 0, 0, 0, 0)
    h2 = Atom("H", 0, 0, 0, 0, 0)
    h3 = Atom("H", 0, 0, 0, 0, 0)
    molecule.addAtom(h1)
    molecule.addAtom(h2)
    molecule.addAtom(h3)
    molecule.addBond(Bond(0, 1, root, h1))
    molecule.addBond(Bond(0, 1, root, h2))
    molecule.addBond(Bond(0, 1, root, h3))
    
    return molecule


def buildWater(anchorAAM, args):
    molecule = Molecule()
    root = Atom("O", 0, 0, 0, 0, 0)
    root.aam = anchorAAM
    molecule.addAtom(root)
    molecule.anchor = root
    h1 = Atom("H", 0, 0, 0, 0, 0)
    h2 = Atom("H", 0, 0, 0, 0, 0)
    molecule.addAtom(h1)
    molecule.addAtom(h2)
    molecule.addBond(Bond(0, 1, root, h1))
    molecule.addBond(Bond(0, 1, root, h2))
    
    return molecule


def buildAlkaliMetal(anchorAAM, args):
    # Not implemented
    return None


PSEUDO = {
        "alkyl" : (
                buildAlkyl,     # function that builds it
                { "size" : [1, 2, 3, 100] }     # arguments the function takes
            ), 
        "halogen" : (buildHalogen, {}), 
        "alkalimetal" : (buildAlkaliMetal, {}),
        "methyl" : (buildAlkyl, { "size" : [1] }),
        "lindlarscatalyst" : (buildLindlarsCatalyst, {}),
        "tso-" : (buildTosylate, {}),
        "nh3" : (buildAmmonia, {}),
        "i-" : (buildIodineAnion, {}),
        "h2o" : (buildWater, {}),
        "roh" : (buildROH, {}),
        "br-" : (buildBromineAnion, {}),
        "x" : (buildHalogen, { "symbol" : ["F", "Cl", "Br", "I"] }),
    }

ATOM_NAMES = {
        "H" : "hydrogen",
        "He" : "helium",
        "Li" : "lithium",
        "Be" : "beryllium",
        "B" : "boron",
        "C" : "carbon",
        "N" : "nitrogen",   
        "O" : "oxygen",
        "F" : "fluorine",
        "Ne" : "neon",
        "Na" : "sodium",
        "Mg" : "magnesium",
        "Al" : "aluminium",
        "Si" : "silicon",
        "P" : "phosphorus",
        "S" : "sulfur", # versus sulphur?
        "Cl" : "chlorine",
        "Ar" : "argon",
        "K" : "potassium",
        "Ca" : "calcium",
        "Sc" : "scandium",
        "Ti" : "titanium",
        "V" : "vanadium",
        "Cr" : "chromium",
        "Mn" : "manganese",
        "Fe" : "iron",
        "Co" : "cobalt",
        "Ni" : "nickel",
        "Cu" : "copper",
        "Zn" : "zink",
        "Ga" : "gallium",
        "Ge" : "germanium",
        "As" : "arsenic",
        "Se" : "selenium",
        "Br" : "bromine",
        "Kr" : "krypton",
        "Rb" : "rubidium",
        "Sr" : "strontium",
        "Y" : "yttrium",
        "Zr" : "zirconium",
        "Nb" : "niobium",
        "Mo" : "molybdenum",
        "Tc" : "technetium",
        "Ru" : "ruthenium",
        "Rh" : "rhodium",
        "Pd" : "palladium",
        "Ag" : "silver",
        "Cd" : "cadmium",
        "In" : "indium",
        "Sn" : "tin",
        "Sb" : "antimony",
        "Te" : "tellurium",
        "I" : "iodine",
        "Xe" : "xenon",
        "Cs" : "caesium",
        "Ba" : "barium",
        # Omitting lanthanoids (57-71)
        "Hf" : "hafnium",
        "Ta" : "tantalum",
        "W" : "tungsten",
        "Re" : "rhenium",
        "Os" : "osmium",
        "Ir" : "iridium",
        "Pt" : "platinum",
        "Au" : "gold",
        "Hg" : "mercury",
        "Tl" : "thallium",
        "Pb" : "lead",
        "Bi" : "bismuth",
        "Po" : "polonium",
        "At" : "astatine",
        "Rn" : "radon",
        "Fr" : "francium",
        "Ra" : "radium"
        # Omitting 89-118+
    }

GROUPS = {
    "halogen": ["cl", "f", "br", "i", "at"],
    "alkalimetal": ["li", "na", "k", "rb", "cs", "fr"],
    "hc": ["h", "c"],
    "hcno": ["h", "c", "n", "o"],
    "r_group": ["halogen", "alkalimetal", "hcno"]
}

# THis is a hack
LIST_TRANSLATION = {
        "C" : "Methyl",
    }
