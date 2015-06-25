(define (problem initialBonds6-D1) (:domain Chemical)
(:objects
h1 - hydrogen
h2 - hydrogen
h3 - hydrogen
h4 - hydrogen
h5 - hydrogen
h6 - hydrogen
c1 - carbon
c2 - carbon
o1 - oxygen
; PBr3 
p1 - phosphorus
br1 - bromine
br2 - bromine
br3 - bromine
)
(:init
(bond c1 c2)
(bond c2 c1)
(bond c2 o1)
(bond o1 c2)
(bond h1 c1)
(bond h2 c1)
(bond h3 c1)
(bond c1 h1)
(bond c1 h2)
(bond c1 h3)
(bond c2 h4)
(bond c2 h5)
(bond h4 c2)
(bond h5 c2)
(bond o1 h6)
(bond h6 o1)
; PBr3 
(bond p1 br1)
(bond p1 br2)
(bond p1 br3)
(bond br1 p1)
(bond br2 p1)
(bond br3 p1)
)
(:goal
(and
(bond c1 c2)
(bond c2 c1)
(bond c1 h1)
(bond h1 c1)
(bond c1 h2)
(bond h2 c1)
(bond c1 h3)
(bond h3 c1)
(bond c2 br1)
(bond br1 c2)
(bond c2 h4)
(bond h4 c2)
(bond c2 h5)
(bond h5 c2)
))
)
