(define (problem initialBonds8-D1) (:domain Chemical)
(:objects
c1 - carbon
c2 - carbon
c3 - carbon
c4 - carbon
c5 - carbon
c6 - carbon
c7 - carbon
c8 - carbon
h1 - hydrogen
h2 - hydrogen
h3 - hydrogen
h4 - hydrogen
h5 - hydrogen
h6 - hydrogen
h7 - hydrogen
h8 - hydrogen
h9 - hydrogen
h10 - hydrogen
h11 - hydrogen
h12 - hydrogen
h13 - hydrogen
h14 - hydrogen
h15 - hydrogen
h16 - hydrogen
; ozone 
o1 - oxygen
o2 - oxygen
o3 - oxygen
)
(:init
(bond c1 c3)
(bond c2 c3)
(bond c3 c1)
(bond c3 c2)
(bond c3 c4)
(bond c4 c3)
(doublebond c4 c5)
(doublebond c5 c4)
(bond c5 c6)
(bond c6 c5)
(bond c6 c7)
(bond c6 c8)
(bond c7 c6)
(bond c8 c6)
(bond h1 c1)
(bond h2 c1)
(bond h3 c1)
(bond c1 h1)
(bond c1 h2)
(bond c1 h3)
(bond h4 c2)
(bond h5 c2)
(bond h6 c2)
(bond c2 h4)
(bond c2 h5)
(bond c2 h6)
(bond h7 c3)
(bond c3 h7)
(bond h8 c4)
(bond c4 h8)
(bond h9 c5)
(bond c5 h9)
(bond h10 c6)
(bond c6 h10)
(bond h11 c7)
(bond h12 c7)
(bond h13 c7)
(bond c7 h11)
(bond c7 h12)
(bond c7 h13)
(bond h14 c8)
(bond h15 c8)
(bond h16 c8)
(bond c8 h14)
(bond c8 h15)
(bond c8 h16)
; ozone 
(bond o1 o2)
(doublebond o1 o3)
(bond o2 o1)
(doublebond o3 o1)
)
(:goal
(and
(bond c1 c3)
(bond c3 c1)
(bond c1 h1)
(bond h1 c1)
(bond c1 h2)
(bond h2 c1)
(bond c1 h3)
(bond h3 c1)
(bond c3 c4)
(bond c4 c3)
(bond c3 h7)
(bond h7 c3)
(bond c4 h8)
(bond h8 c4)
(doublebond c4 o2)
(doublebond o2 c4)
))
)
