(define (problem initialBonds13) (:domain Chemical)
(:objects
; setup for problem 13 
h1 - hydrogen
h2 - hydrogen
h3 - hydrogen
h4 - hydrogen
h5 - hydrogen
h6 - hydrogen
h7 - hydrogen
h8 - hydrogen
o1 - oxygen
o2 - oxygen
c1 - carbon
c2 - carbon
c3 - carbon
c4 - carbon
; The second starting material 
h9 - hydrogen
h10 - hydrogen
h11 - hydrogen
h12 - hydrogen
h13 - hydrogen
h14 - hydrogen
h15 - hydrogen
h16 - hydrogen
o3 - oxygen
o4 - oxygen
c5 - carbon
c6 - carbon
c7 - carbon
c8 - carbon
; The next compound 
c9 - carbon
c10 - carbon
c11 - carbon
c12 - carbon
c13 - carbon
h17 - hydrogen
h18 - hydrogen
h19 - hydrogen
h20 - hydrogen
h21 - hydrogen
h22 - hydrogen
h23 - hydrogen
h24 - hydrogen
h25 - hydrogen
h26 - hydrogen
br1 - bromine
br2 - bromine
; water 
h27 - hydrogen
h28 - hydrogen
o5 - oxygen
; strong base 
na1 - sodium
h29 - hydrogen
)
(:init
; setup for problem 13 
(bond c1 c2)
(bond c2 c1)
(bond c2 o1)
(bond o1 c2)
(bond o1 c3)
(bond c3 o1)
(doublebond c3 o2)
(doublebond o2 c3)
(bond c3 c4)
(bond c3 c4)
(bond c1 h1)
(bond c1 h2)
(bond c1 h3)
(bond h1 c1)
(bond h2 c1)
(bond h3 c1)
(bond c2 h4)
(bond c2 h5)
(bond h4 c2)
(bond h5 c2)
(bond c4 h6)
(bond c4 h7)
(bond c4 h8)
(bond h6 c4)
(bond h7 c4)
(bond h8 c4)
; The second starting material 
(bond c5 c6)
(bond c6 c5)
(bond c6 o3)
(bond o3 c6)
(bond o3 c7)
(bond c7 o3)
(doublebond c7 o4)
(doublebond o4 c7)
(bond c7 c8)
(bond c8 c7)
(bond c5 h9)
(bond c5 h10)
(bond c5 h11)
(bond h9 c5)
(bond h10 c5)
(bond h11 c5)
(bond c6 h12)
(bond c6 h13)
(bond h12 c6)
(bond h13 c6)
(bond c8 h14)
(bond c8 h15)
(bond c8 h16)
(bond h14 c8)
(bond h15 c8)
(bond h16 c8)
; The next compound 
(bond b1 c9)
(bond c9 c10)
(bond c10 c11)
(bond c11 c12)
(bond c12 c13)
(bond c13 br2)
(bond c9 br1)
(bond c10 c9)
(bond c11 c10)
(bond c12 c11)
(bond c13 c12)
(bond br2 c13)
(bond c9 h17)
(bond c9 h18)
(bond c10 h19)
(bond c10 h20)
(bond c11 h21)
(bond c11 h22)
(bond c12 h23)
(bond c12 h24)
(bond c13 h25)
(bond c13 h26)
(bond h17 c9)
(bond h18 c9)
(bond h19 c10)
(bond h20 c10)
(bond h21 c11)
(bond h22 c11)
(bond h23 c12)
(bond h24 c12)
(bond h25 c13)
(bond h26 c13)
; water 
(bond o5 h27)
(bond o5 h28)
(bond h27 o5)
(bond h28 o5)
; strong base 
(bond na1 h29)
(bond h29 na1)
)
(:goal
(and
(bond c8 c9)
(bond c9 c10)
(bond c10 c11)
(bond c11 c12)
(bond c12 c13)
(bond c13 c8)
(bond c8 c3)
(doublebond c3 o2)
(bond c3 c4)
(bond c8 h27)
(bond c9 h17)
(bond c9 h18)
(bond h19 c10)
(bond c10 h20)
(bond h21 c11)
(bond h22 c11)
(bond c12 h23)
(bond c12 h24)
(bond h25 c13)
(bond c13 h26)
(bond c4 h6)
(bond c4 h7)
(bond c4 h8)
)
)
)