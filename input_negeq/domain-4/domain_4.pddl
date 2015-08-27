(define (domain Chemical)
(:requirements :strips :typing)
(:types chemical_atom - object
        phosphorus sulfur magnesium aluminium chromium iron manganese mercury boron copper
        r_group - chemical_atom
        halogen alkalimetal hcno - r_group
        hc nitrogen oxygen - hcno
        hydrogen carbon - hc
        chlorine fluorine bromine iodine astatine - halogen
        lithium sodium potassium rubidium caesium francium - alkalimetal
        )

(:predicates
    (bond ?x - chemical_atom ?y - chemical_atom)
    (doublebond ?x - chemical_atom ?y - chemical_atom)
    (triplebond ?x - chemical_atom ?y - chemical_atom)
    (aromaticbond ?x - chemical_atom ?y - chemical_atom)
    (distinct ?x - chemical_atom ?y - chemical_atom)
    )
    
(:action alcoholandpbr
    :parameters (?o_5 - oxygen ?br_4 - bromine ?c_7 - carbon ?p_1 - phosphorus ?br_3 - bromine ?br_2 - bromine ?h_6 - hydrogen)
    :precondition (and (distinct ?br_2 ?br_3) (distinct ?br_2 ?br_4) (distinct ?br_4 ?br_3) (bond ?br_2 ?p_1) (bond ?p_1 ?br_4) (bond ?p_1 ?br_3) (bond ?h_6 ?o_5) (bond ?o_5 ?c_7))
    :effect (and (not (bond ?p_1 ?br_4)) (not (bond ?br_4 ?p_1)) (bond ?p_1 ?o_5) (bond ?o_5 ?p_1) (bond ?br_4 ?c_7) (bond ?c_7 ?br_4) (not (bond ?o_5 ?c_7)) (not (bond ?c_7 ?o_5))))

(:action alkeneandwater
    :parameters (?o_1 - oxygen ?h_2 - hydrogen ?c_4 - carbon ?c_5 - carbon ?h_3 - hydrogen)
    :precondition (and (distinct ?c_5 ?c_4) (distinct ?h_2 ?h_3) (bond ?h_2 ?o_1) (bond ?h_3 ?o_1) (doubleBond ?c_5 ?c_4))
    :effect (and (not (bond ?h_2 ?o_1)) (not (bond ?o_1 ?h_2)) (bond ?o_1 ?c_5) (bond ?c_5 ?o_1) (bond ?h_2 ?c_4) (bond ?c_4 ?h_2) (not (doubleBond ?c_5 ?c_4)) (not (doubleBond ?c_4 ?c_5)) (bond ?c_5 ?c_4) (bond ?c_4 ?c_5)))

(:action dielsalder
    :parameters (?c_1 - carbon ?c_3 - carbon ?c_2 - carbon ?c_5 - carbon ?c_4 - carbon ?c_6 - carbon )
    :precondition (and (distinct ?c_1 ?c_2) (distinct ?c_1 ?c_4) (distinct ?c_1 ?c_3) (distinct ?c_1 ?c_6) (distinct ?c_1 ?c_5) (distinct ?c_2 ?c_4) (distinct ?c_2 ?c_3) (distinct ?c_2 ?c_6) (distinct ?c_2 ?c_5) (distinct ?c_4 ?c_3) (distinct ?c_4 ?c_6) (distinct ?c_4 ?c_5) (distinct ?c_3 ?c_6) (distinct ?c_3 ?c_5) (distinct ?c_6 ?c_5) (bond ?c_1 ?c_2) (doubleBond ?c_4 ?c_1) (doubleBond ?c_3 ?c_2) (doubleBond ?c_6 ?c_5))
    :effect (and (not (bond ?c_1 ?c_2)) (not (bond ?c_2 ?c_1)) (doubleBond ?c_1 ?c_2) (doubleBond ?c_2 ?c_1) (not (doubleBond ?c_4 ?c_1)) (not (doubleBond ?c_1 ?c_4)) (bond ?c_4 ?c_1) (bond ?c_1 ?c_4) (not (doubleBond ?c_3 ?c_2)) (not (doubleBond ?c_2 ?c_3)) (bond ?c_3 ?c_2) (bond ?c_2 ?c_3) (bond ?c_6 ?c_3) (bond ?c_3 ?c_6) (bond ?c_4 ?c_5) (bond ?c_5 ?c_4) (not (doubleBond ?c_6 ?c_5)) (not (doubleBond ?c_5 ?c_6)) (bond ?c_6 ?c_5) (bond ?c_5 ?c_6)))

(:action ozonolysis
    :parameters (?c_5 - carbon ?o_1 - oxygen ?c_4 - carbon ?o_3 - oxygen ?o_2 - oxygen )
    :precondition (and (distinct ?c_5 ?c_4) (distinct ?o_2 ?o_1) (distinct ?o_2 ?o_3) (distinct ?o_1 ?o_3) (doubleBond ?o_2 ?o_1) (bond ?o_2 ?o_3) (doubleBond ?c_5 ?c_4))
    :effect (and (not (doubleBond ?o_2 ?o_1)) (not (doubleBond ?o_1 ?o_2)) (doubleBond ?c_5 ?o_1) (doubleBond ?o_1 ?c_5) (not (bond ?o_2 ?o_3)) (not (bond ?o_3 ?o_2)) (doubleBond ?c_4 ?o_3) (doubleBond ?o_3 ?c_4) (not (doubleBond ?c_5 ?c_4)) (not (doubleBond ?c_4 ?c_5))))
)
