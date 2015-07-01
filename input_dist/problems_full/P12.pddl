(define (problem initialBonds12) (:domain Chemical)
(:objects
; setup for problem 12 
h1 - hydrogen
h2 - hydrogen
h3 - hydrogen
h4 - hydrogen
h5 - hydrogen
h6 - hydrogen
h7 - hydrogen
h8 - hydrogen
c1 - carbon
c2 - carbon
c3 - carbon
c4 - carbon
c5 - carbon
; The ketone 
c6 - carbon
c7 - carbon
c8 - carbon
c9 - carbon
h9 - hydrogen
h10 - hydrogen
h11 - hydrogen
h12 - hydrogen
h13 - hydrogen
h14 - hydrogen
o1 - oxygen
; H2 
h15 - hydrogen
h16 - hydrogen
; palladium 
pd1 - palladium
; water 
h18 - hydrogen
h19 - hydrogen
o2 - oxygen
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
; Benzene 
c10 - carbon
c11 - carbon
c12 - carbon
c13 - carbon
c14 - carbon
c15 - carbon
h20 - hydrogen
h21 - hydrogen
h22 - hydrogen
h23 - hydrogen
h24 - hydrogen
h25 - hydrogen
; second benzene
c16 - carbon
c17 - carbon
c18 - carbon
c19 - carbon
c20 - carbon
c21 - carbon
h26 - hydrogen
h27 - hydrogen
h28 - hydrogen
h29 - hydrogen
h30 - hydrogen
h31 - hydrogen
; FeBr3 
fe1 - iron
br1 - bromine
br2 - bromine
br3 - bromine
; Br2 
br4 - bromine
br5 - bromine
; second Br2 
br9 - bromine
br10 - bromine
; free mg 
mg1 - magnesium
; second free mg
mg2 - magnesium
; free hydrogen 
h32 - hydrogen
)
(:init
; setup for problem 12 
(doublebond c1 c2)
(bond c2 c3)
(doublebond c3 c4)
(bond c4 c5)
(doublebond c2 c1)
(bond c3 c2)
(doublebond c4 c3)
(bond c5 c4)
(bond c1 h1)
(bond c1 h2)
(bond c2 h3)
(bond c3 h4)
(bond c4 h5)
(bond c5 h6)
(bond c5 h7)
(bond c5 h8)
(bond h1 c1)
(bond h2 c1)
(bond h3 c2)
(bond h4 c3)
(bond h5 c4)
(bond h6 c5)
(bond h7 c5)
(bond h8 c5)
; The ketone 
(bond c6 c7)
(doublebond c7 c8)
(bond c8 c9)
(bond c7 c6)
(doublebond c8 c7)
(bond c9 c8)
(bond c6 h9)
(bond c6 h10)
(bond c6 h11)
(bond h9 c6)
(bond h10 c6)
(bond h11 c6)
(bond c7 h12)
(bond c8 h13)
(bond c9 h14)
(bond h12 c7)
(bond h13 c8)
(bond h14 c9)
(doublebond o1 c9)
(doublebond c9 o1)
; H2 
(bond h15 h16)
(bond h16 h15)
; palladium 
; water 
(bond o2 h18)
(bond o2 h19)
(bond h18 o2)
(bond h19 o2)
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
; Benzene 
(doublebond c10 c11)
(doublebond c11 c10)
(bond c11 c12)
(bond c12 c11)
(doublebond c12 c13)
(doublebond c13 c12)
(bond c13 c14)
(bond c14 c13)
(doublebond c14 c15)
(doublebond c15 c14)
(bond c10 c15)
(bond c15 c10)
(bond c10 h20)
(bond h20 c10)
(bond c11 h21)
(bond h21 c11)
(bond c12 h22)
(bond h22 c12)
(bond c13 h23)
(bond h23 c13)
(bond c14 h24)
(bond h24 c14)
(bond c15 h25)
(bond h25 c15)
; second benzene
(doublebond c16 c17)
(doublebond c17 c16)
(bond c17 c18)
(bond c18 c17)
(doublebond c18 c19)
(doublebond c19 c18)
(bond c19 c20)
(bond c20 c19)
(doublebond c20 c21)
(doublebond c21 c20)
(bond c16 c21)
(bond c21 c16)
(bond c16 h26)
(bond h26 c16)
(bond c17 h27)
(bond h27 c17)
(bond c18 h28)
(bond h28 c18)
(bond c19 h29)
(bond h29 c19)
(bond c20 h30)
(bond h30 c20)
(bond c21 h31)
(bond h31 c21)
; FeBr3 
(bond fe1 br1)
(bond fe1 br2)
(bond fe1 br3)
(bond br1 fe1)
(bond br2 fe1)
(bond br3 fe1)
; Br2 
(bond br4 br5)
(bond br5 br4)
; second Br2 
(bond br9 br10)
(bond br10 br9)
; free mg 
; second free mg
; free hydrogen 
)
(:goal
(and
(bond c4 c5)
(bond c4 c3)
(bond c3 c2)
(bond c2 c1)
(bond c1 c7)
(bond c7 c6)
(bond c7 c8)
(bond c4 c8)
(bond c8 c9)
(bond c9 c10)
(doublebond c10 c11)
(bond c11 c12)
(doublebond c12 c13)
(bond c13 c14)
(doublebond c14 c15)
(bond c10 c15)
(bond c9 c16)
(doublebond c16 c17)
(bond c17 c18)
(doublebond c18 c19)
(bond c19 c20)
(doublebond c20 c21)
(bond c16 c21)
(bond c9 o1)
(bond c4 h5)
(bond c5 h6)
(bond c5 h7)
(bond c5 h8)
(bond c3 h4)
(bond c3 h16)
(bond c2 h3)
(bond c2 h15)
(bond c1 h1)
(bond c1 h2)
(bond c7 h12)
(bond c6 h9)
(bond c6 h10)
(bond c6 h11)
(bond c8 h13)
(bond c11 h21)
(bond c12 h22)
(bond c13 h23)
(bond c14 h24)
(bond c15 h25)
(bond c17 h27)
(bond c18 h28)
(bond c19 h29)
(bond c20 h30)
(bond c21 h31)
(bond o1 h32)
)
)
)