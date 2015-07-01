(define (problem initialBonds8) (:domain Chemical)
(:objects
; setup for problem 8 
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
; Na2Cr2O7 
na1 - sodium
na2 - sodium
cr1 - chromium
cr2 - chromium
o7 - oxygen
o8 - oxygen
o9 - oxygen
o10 - oxygen
o11 - oxygen
o12 - oxygen
o13 - oxygen
; Thionyl chloride 
su1 - sulfur
o4 - oxygen
cl1 - chlorine
cl2 - chlorine
; Ammonia 
n1 - nitrogen
h17 - hydrogen
h18 - hydrogen
h19 - hydrogen
; phosphorylChloride 
p1 - phosphor
o5 - oxygen
cl3 - chlorine
cl4 - chlorine
cl5 - chlorine
; water 
o6 - oxygen
h20 - hydrogen
h21 - hydrogen
)
(:init
; setup for problem 8 
(bond c1 c3)
(bond c2 c3)
(bond c3 c1)
(bond c3 c1)
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
; Na2Cr2O7 
(bond cr1 o7)
(bond cr2 o7)
(bond o7 cr1)
(bond o7 cr2)
(doublebond cr1 o8)
(doublebond cr1 o9)
(doublebond cr1 o10)
(doublebond o8 cr1)
(doublebond o9 cr1)
(doublebond o10 cr1)
(doublebond cr2 o11)
(doublebond cr2 o12)
(doublebond cr2 o13)
(doublebond o11 cr2)
(doublebond o12 cr2)
(doublebond o13 cr2)
(bond na1 cr1)
(bond na2 cr2)
(bond cr1 na1)
(bond cr2 na2)
; Thionyl chloride 
(doublebond su1 o4)
(doublebond o4 su1)
(bond cl1 su1)
(bond cl2 su1)
(bond su1 cl1)
(bond su1 cl2)
; Ammonia 
(bond n1 h17)
(bond n1 h18)
(bond n1 h19)
(bond h17 n1)
(bond h18 n1)
(bond h19 n1)
; phosphorylChloride 
(doublebond p1 o5)
(doublebond o5 p1)
(bond cl3 p1)
(bond cl4 p1)
(bond cl5 p1)
(bond p1 cl3)
(bond p1 cl4)
(bond p1 cl5)
; water 
(bond o6 h20)
(bond o6 h21)
(bond h20 o6)
(bond h21 o6)
)
(:goal
(and
(bond c2 c3)
(bond c3 c1)
(bond c3 c4)
(triplebond c4 n1)
(bond c2 h4)
(bond c2 h5)
(bond c2 h6)
(bond c3 h7)
(bond c1 h1)
(bond c1 h2)
(bond c1 h3)
)
)
)