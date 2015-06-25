(define (problem initialBonds3-D1) (:domain Chemical)
(:objects
h1 - hydrogen
h2 - hydrogen
h3 - hydrogen
h4 - hydrogen
h19 - hydrogen
h20 - hydrogen
h21 - hydrogen
h22 - hydrogen
c1 - carbon
c2 - carbon
c3 - carbon
o1 - oxygen
; PBr3 
p - phosphorus
br1 - bromine
br2 - bromine
br3 - bromine
)
(:init
(bond c1 c2)
(bond c2 c3)
(bond c2 c1)
(bond c3 c2)
(bond o1 c3)
(bond c3 o1)
(bond c1 h1)
(bond c1 h2)
(bond c1 h3)
(bond h1 c1)
(bond h2 c1)
(bond h3 c1)
(bond h4 o1)
(bond o1 h4)
(bond h19 c2)
(bond h20 c2)
(bond h21 c3)
(bond h22 c3)
(bond c2 h19)
(bond c2 h20)
(bond c3 h21)
(bond c3 h22)
; PBr3 
(bond p br1)
(bond p br2)
(bond p br3)
(bond br1 p)
(bond br2 p)
(bond br3 p)
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
(bond c2 c3)
(bond c3 c2)
(bond c2 h19)
(bond h19 c2)
(bond c2 h20)
(bond h20 c2)
(bond c3 br1)
(bond br1 c3)
(bond c3 h21)
(bond h21 c3)
(bond c3 h22)
(bond h22 c3)
))
)