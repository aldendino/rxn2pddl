(define (problem initialBonds10-D1) (:domain Chemical)
(:objects
c1 - carbon
c2 - carbon
c3 - carbon
c4 - carbon
h1 - hydrogen
h2 - hydrogen
o1 - oxygen
o2 - oxygen
o3 - oxygen
; the Diene 
c5 - carbon
c6 - carbon
c8 - carbon
c7 - carbon
;arbon(c8
c9 - carbon
c14 - carbon
h3 - hydrogen
h4 - hydrogen
h5 - hydrogen
h6 - hydrogen
h7 - hydrogen
h8 - hydrogen
h9 - hydrogen
h10 - hydrogen
h29 - hydrogen
h30 - hydrogen
h31 - hydrogen
;ond(h8,c8,[]
;ond(c8,h8,[]
)
(:init
(bond o1 c1)
(bond o1 c2)
(bond c1 o1)
(bond c2 o1)
(doublebond o2 c1)
(doublebond o3 c2)
(doublebond c1 o2)
(doublebond c2 o3)
(bond c1 c3)
(bond c2 c4)
(bond c3 c1)
(bond c4 c2)
(doublebond c3 c4)
(doublebond c4 c3)
(bond h1 c3)
(bond h2 c4)
(bond c3 h1)
(bond c4 h2)
; the Diene 
;arbon(c8
(bond c5 c6)
(doublebond c6 c7)
(bond c7 c8)
(doublebond c8 c9)
(bond c6 c5)
(doublebond c7 c6)
(bond c8 c7)
(doublebond c9 c8)
(bond c8 c14)
(bond c14 c8)
(bond h3 c5)
(bond h4 c5)
(bond h5 c5)
(bond c5 h3)
(bond c5 h4)
(bond c5 h5)
(bond h6 c6)
(bond c6 h6)
(bond h7 c7)
(bond c7 h7)
;ond(h8,c8,[]
;ond(c8,h8,[]
(bond c9 h9)
(bond c9 h10)
(bond h9 c9)
(bond h10 c9)
(bond c14 h29)
(bond c14 h30)
(bond c14 h31)
(bond h29 c14)
(bond h30 c14)
(bond h31 c14)
)
(:goal
(and
(bond c1 c3)
(bond c3 c1)
(bond c1 o1)
(bond o1 c1)
(doublebond c1 o2)
(doublebond o2 c1)
(bond c3 c4)
(bond c4 c3)
(bond c3 c6)
(bond c6 c3)
(bond c3 h1)
(bond h1 c3)
(bond c4 c2)
(bond c2 c4)
(bond c4 c9)
(bond c9 c4)
(bond c4 h2)
(bond h2 c4)
(bond c2 o1)
(bond o1 c2)
(doublebond c2 o3)
(doublebond o3 c2)
(bond c9 c8)
(bond c8 c9)
(bond c9 h10)
(bond h10 c9)
(bond c9 h9)
(bond h9 c9)
(bond c8 c14)
(bond c14 c8)
(doublebond c8 c7)
(doublebond c7 c8)
(bond c14 h29)
(bond h29 c14)
(bond c14 h30)
(bond h30 c14)
(bond c14 h31)
(bond h31 c14)
(bond c7 c6)
(bond c6 c7)
(bond c7 h7)
(bond h7 c7)
(bond c6 c5)
(bond c5 c6)
(bond c6 h6)
(bond h6 c6)
(bond c5 h3)
(bond h3 c5)
(bond c5 h4)
(bond h4 c5)
(bond c5 h5)
(bond h5 c5)
))
)