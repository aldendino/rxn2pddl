(define (problem initialBonds17-D1) (:domain Chemical)
(:objects
; setup for problem 17 
c1 - carbon
c2 - carbon
c3 - carbon
c4 - carbon
c5 - carbon
c6 - carbon
o1 - oxygen
h1 - hydrogen
h2 - hydrogen
h3 - hydrogen
h4 - hydrogen
h5 - hydrogen
h6 - hydrogen
h7 - hydrogen
h8 - hydrogen
h27 - hydrogen
h28 - hydrogen
h29 - hydrogen
h30 - hydrogen
; first PCC 
c12 - carbon
c13 - carbon
c14 - carbon
c15 - carbon
c16 - carbon
n4 - nitrogen
h9 - hydrogen
h10 - hydrogen
h11 - hydrogen
h12 - hydrogen
h13 - hydrogen
h14 - hydrogen
cr1 - chromium
o4 - oxygen
o5 - oxygen
o6 - oxygen
cl1 - chlorine
)
(:init
; setup for problem 17 
(bond c1 c2)
(bond c2 c3)
(bond c3 c4)
(bond c4 c5)
(bond c5 c6)
(bond c1 c6)
(bond c2 c1)
(bond c3 c2)
(bond c4 c3)
(bond c5 c4)
(bond c6 c5)
(bond c6 c1)
(bond c1 o1)
(bond o1 c1)
(bond c1 h1)
(bond h1 c1)
(bond c2 h2)
(bond c2 h3)
(bond c3 h4)
(bond c3 h5)
(bond c4 h6)
(bond c4 h7)
(bond c5 h8)
(bond c5 h27)
(bond c6 h28)
(bond c6 h29)
(bond h2 c2)
(bond h3 c2)
(bond h4 c3)
(bond h5 c3)
(bond h6 c4)
(bond h7 c4)
(bond h8 c5)
(bond h27 c5)
(bond h28 c6)
(bond h29 c6)
(bond o1 h30)
(bond h30 o1)
; first PCC 
(bond n4 h9)
(bond h9 n4)
(doublebond c12 n4)
(bond c12 c13)
(doublebond c13 c14)
(bond c14 c15)
(doublebond c15 c16)
(bond c16 n4)
(doublebond n4 c12)
(bond c13 c12)
(doublebond c14 c13)
(bond c15 c14)
(doublebond c16 c15)
(bond n4 c16)
(bond h10 c12)
(bond h11 c13)
(bond h12 c14)
(bond h13 c15)
(bond h14 c16)
(bond c12 h10)
(bond c13 h11)
(bond c14 h12)
(bond c15 h13)
(bond c16 h14)
(bond o4 cr1)
(doublebond cr1 o5)
(doublebond cr1 o6)
(bond cr1 cl1)
(bond cr1 o4)
(doublebond o5 cr1)
(doublebond o6 cr1)
(bond cl1 cr1)
(bond n4 o4)
(bond o4 n4)
)
(:goal
(and
(bond c1 c2)
(bond c2 c1)
(bond c1 c6)
(bond c6 c1)
(doublebond c1 o1)
(doublebond o1 c1)
(bond c2 c3)
(bond c3 c2)
(bond c2 h2)
(bond h2 c2)
(bond c2 h3)
(bond h3 c2)
(bond c3 c4)
(bond c4 c3)
(bond c3 h4)
(bond h4 c3)
(bond c3 h5)
(bond h5 c3)
(bond c4 c5)
(bond c5 c4)
(bond c4 h6)
(bond h6 c4)
(bond c4 h7)
(bond h7 c4)
(bond c5 c6)
(bond c6 c5)
(bond c5 h27)
(bond h27 c5)
(bond c5 h8)
(bond h8 c5)
(bond c6 h28)
(bond h28 c6)
(bond c6 h29)
(bond h29 c6)
))
)