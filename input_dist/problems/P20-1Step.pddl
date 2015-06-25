(define (problem initialBonds20-D1) (:domain Chemical)
(:objects
c1 - carbon
c2 - carbon
c3 - carbon
c4 - carbon
c5 - carbon
c6 - carbon
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
; water 
o1 - oxygen
h11 - hydrogen
h12 - hydrogen
)
(:init
(doublebond c1 c2)
(doublebond c2 c1)
(bond c2 c3)
(bond c3 c4)
(bond c4 c5)
(bond c5 c6)
(bond c6 c1)
(bond c3 c2)
(bond c4 c3)
(bond c5 c4)
(bond c6 c5)
(bond c1 c6)
(bond h1 c1)
(bond h2 c2)
(bond c1 h1)
(bond c2 h2)
(bond h3 c3)
(bond h4 c3)
(bond h5 c4)
(bond h6 c4)
(bond h7 c5)
(bond h8 c5)
(bond h9 c6)
(bond h10 c6)
(bond c3 h3)
(bond c3 h4)
(bond c4 h5)
(bond c4 h6)
(bond c5 h7)
(bond c5 h8)
(bond c6 h9)
(bond c6 h10)
; water 
(bond h11 o1)
(bond h12 o1)
(bond o1 h11)
(bond o1 h12)
)
(:goal
(and
(bond c1 c2)
(bond c2 c1)
(bond c1 c6)
(bond c6 c1)
(bond c1 h1)
(bond h1 c1)
(bond c1 h11)
(bond h11 c1)
(bond c2 c3)
(bond c3 c2)
(bond c2 h2)
(bond h2 c2)
(bond c2 o1)
(bond o1 c2)
(bond c3 c4)
(bond c4 c3)
(bond c3 h3)
(bond h3 c3)
(bond c3 h4)
(bond h4 c3)
(bond c4 c5)
(bond c5 c4)
(bond c4 h5)
(bond h5 c4)
(bond c4 h6)
(bond h6 c4)
(bond c5 c6)
(bond c6 c5)
(bond c5 h7)
(bond h7 c5)
(bond c5 h8)
(bond h8 c5)
(bond c6 h10)
(bond h10 c6)
(bond c6 h9)
(bond h9 c6)
(bond o1 h12)
(bond h12 o1)
))
)