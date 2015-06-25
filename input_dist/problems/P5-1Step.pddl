(define (problem initialBonds5-D1) (:domain Chemical)
(:objects
c1 - carbon
c2 - carbon
c3 - carbon
o1 - oxygen
h1 - hydrogen
h2 - hydrogen
h3 - hydrogen
h4 - hydrogen
h5 - hydrogen
h6 - hydrogen
h7 - hydrogen
h8 - hydrogen
;  PCC 
c17 - carbon
c18 - carbon
c19 - carbon
c20 - carbon
c21 - carbon
n5 - nitrogen
h17 - hydrogen
h18 - hydrogen
h19 - hydrogen
h20 - hydrogen
h21 - hydrogen
h22 - hydrogen
cr2 - chromium
o7 - oxygen
o8 - oxygen
o9 - oxygen
cl2 - chlorine
)
(:init
(bond c1 c2)
(bond c2 c1)
(bond c2 c3)
(bond c3 c2)
(bond c2 o1)
(bond o1 c2)
(bond c1 h1)
(bond h1 c1)
(bond c1 h2)
(bond h2 c1)
(bond c1 h3)
(bond h3 c1)
(bond c2 h4)
(bond h4 c2)
(bond c3 h5)
(bond h5 c3)
(bond c3 h6)
(bond h6 c3)
(bond c3 h7)
(bond h7 c3)
(bond o1 h8)
(bond h8 o1)
;  PCC 
(bond n5 h19)
(bond h19 n5)
(doublebond c17 n5)
(bond c17 c18)
(doublebond c18 c19)
(bond c19 c20)
(doublebond c20 c21)
(bond c21 n5)
(doublebond n5 c17)
(bond c18 c17)
(doublebond c19 c18)
(bond c20 c19)
(doublebond c21 c20)
(bond n5 c21)
(bond h18 c17)
(bond h17 c18)
(bond h20 c19)
(bond h21 c20)
(bond h22 c21)
(bond c17 h18)
(bond c18 h17)
(bond c19 h20)
(bond c20 h21)
(bond c21 h22)
(bond o7 cr2)
(doublebond cr2 o8)
(doublebond cr2 o9)
(bond cr2 cl2)
(bond cr2 o7)
(doublebond o8 cr2)
(doublebond o9 cr2)
(bond cl2 cr2)
(bond n5 o7)
(bond o7 n5)
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
(doublebond c2 o1)
(doublebond o1 c2)
(bond c3 h5)
(bond h5 c3)
(bond c3 h6)
(bond h6 c3)
(bond c3 h7)
(bond h7 c3)
))
)
