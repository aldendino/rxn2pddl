(define (problem initialBonds14-2-D1) (:domain Chemical)
(:objects
; second isopropanol 
h15 - hydrogen
h16 - hydrogen
h17 - hydrogen
h18 - hydrogen
h19 - hydrogen
h20 - hydrogen
h21 - hydrogen
h22 - hydrogen
o2 - oxygen
c4 - carbon
c5 - carbon
c6 - carbon
; PBr3
p1 - phosphorus
br1 - bromine
br2 - bromine
br3 - bromine
)
(:init
; second isopropanol 
(bond c4 c5)
(bond c5 c4)
(bond c5 o2)
(bond o2 c5)
(bond c5 c6)
(bond c6 c5)
(bond c4 h15)
(bond c4 h16)
(bond c4 h17)
(bond h15 c4)
(bond h16 c4)
(bond h17 c4)
(bond c5 h18)
(bond h18 c5)
(bond c6 h20)
(bond c6 h21)
(bond c6 h22)
(bond h20 c6)
(bond h21 c6)
(bond h22 c6)
(bond o2 h19)
(bond h19 o2)
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
(bond br1 c5)
(bond c5 br1)
(bond c5 c4)
(bond c4 c5)
(bond c5 c6)
(bond c6 c5)
(bond c5 h18)
(bond h18 c5)
(bond c4 h15)
(bond h15 c4)
(bond c4 h16)
(bond h16 c4)
(bond c4 h17)
(bond h17 c4)
(bond c6 h20)
(bond h20 c6)
(bond c6 h21)
(bond h21 c6)
(bond c6 h22)
(bond h22 c6)
))
)
