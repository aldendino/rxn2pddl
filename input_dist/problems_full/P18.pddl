(define (problem initialBonds18) (:domain Chemical)
(:objects
; maleic anhydride 
c1 - carbon
c2 - carbon
c3 - carbon
c4 - carbon
o1 - oxygen
o2 - oxygen
o3 - oxygen
h1 - hydrogen
h2 - hydrogen
; second starting material 
c5 - carbon
c6 - carbon
c7 - carbon
c8 - carbon
c9 - carbon
c10 - carbon
c11 - carbon
c12 - carbon
c13 - carbon
c14 - carbon
c15 - carbon
c16 - carbon
c17 - carbon
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
o4 - oxygen
; ozone 
o5 - oxygen
o6 - oxygen
o7 - oxygen
; LiAlH4
li1 - lithium
al1 - aluminium
h37 - hydrogen
h38 - hydrogen
h39 - hydrogen
h40 - hydrogen
; second LiAlH4
li2 - lithium
al2 - aluminium
h41 - hydrogen
h42 - hydrogen
h43 - hydrogen
h44 - hydrogen
; third LiAlH4
li3 - lithium
al3 - aluminium
h45 - hydrogen
h46 - hydrogen
h47 - hydrogen
h48 - hydrogen
; fourth LiAlH4
li4 - lithium
al4 - aluminium
h49 - hydrogen
h50 - hydrogen
h51 - hydrogen
h52 - hydrogen
; first BnBr 
br1 - bromine
c18 - carbon
c19 - carbon
c20 - carbon
c21 - carbon
c22 - carbon
c23 - carbon
c24 - carbon
h17 - hydrogen
h18 - hydrogen
h19 - hydrogen
h20 - hydrogen
h21 - hydrogen
h22 - hydrogen
h23 - hydrogen
; second BnBr 
br2 - bromine
c25 - carbon
c26 - carbon
c27 - carbon
c28 - carbon
c29 - carbon
c30 - carbon
c31 - carbon
h24 - hydrogen
h25 - hydrogen
h26 - hydrogen
h27 - hydrogen
h28 - hydrogen
h29 - hydrogen
h30 - hydrogen
; third BnBr 
br3 - bromine
c32 - carbon
c33 - carbon
c34 - carbon
c35 - carbon
c36 - carbon
c37 - carbon
c38 - carbon
h53 - hydrogen
h54 - hydrogen
h55 - hydrogen
h56 - hydrogen
h57 - hydrogen
h58 - hydrogen
h59 - hydrogen
; fourth BnBr 
br4 - bromine
c39 - carbon
c40 - carbon
c41 - carbon
c42 - carbon
c43 - carbon
c44 - carbon
c45 - carbon
h60 - hydrogen
h61 - hydrogen
h62 - hydrogen
h63 - hydrogen
h64 - hydrogen
h65 - hydrogen
h66 - hydrogen
)
(:init
; maleic anhydride 
(doublebond c1 c2)
(doublebond c2 c1)
(bond c3 c1)
(bond c1 c3)
(bond c2 c4)
(bond c4 c2)
(doublebond c3 o1)
(doublebond o1 c3)
(bond c3 o2)
(bond o2 c3)
(bond o2 c4)
(bond c4 o2)
(doublebond c4 o3)
(doublebond o3 c4)
(bond c1 h1)
(bond c2 h2)
(bond h1 c1)
(bond h2 c2)
; second starting material 
(bond c5 c6)
(doublebond c6 c7)
(bond c7 c8)
(doublebond c8 c9)
(bond c9 c10)
(doublebond c10 c5)
(bond c6 c5)
(doublebond c7 c6)
(bond c8 c7)
(doublebond c9 c8)
(bond c10 c9)
(doublebond c5 c10)
(bond c5 c11)
(bond c11 c5)
(bond c11 o4)
(bond o4 c11)
(bond o4 c12)
(bond c12 o4)
(bond c12 c13)
(bond c13 c12)
(bond c13 c14)
(doublebond c14 c15)
(bond c15 c16)
(doublebond c16 c17)
(bond c17 c13)
(bond c14 c13)
(doublebond c15 c14)
(bond c16 c15)
(doublebond c17 c16)
(bond c13 c17)
(bond c6 h3)
(bond c7 h4)
(bond c8 h5)
(bond c9 h6)
(bond c10 h7)
(bond h3 c6)
(bond h4 c7)
(bond h5 c8)
(bond h6 c9)
(bond h7 c10)
(bond h8 c11)
(bond h9 c11)
(bond c11 h8)
(bond c11 h9)
(bond h10 c12)
(bond h11 c12)
(bond c12 h10)
(bond c12 h11)
(bond c13 h12)
(bond c14 h13)
(bond c15 h14)
(bond c16 h15)
(bond c17 h16)
(bond h12 c13)
(bond h13 c14)
(bond h14 c15)
(bond h15 c16)
(bond h16 c17)
; ozone 
(bond o5 o6)
(doublebond o5 o7)
(bond o6 o5)
(doublebond o7 o5)
; LiAlH4
(bond al1 li1)
(bond al1 h37)
(bond al1 h38)
(bond al1 h39)
(bond al1 h40)
(bond li1 al1)
(bond h37 al1)
(bond h38 al1)
(bond h39 al1)
(bond h40 al1)
; second LiAlH4
(bond al2 li2)
(bond al2 h41)
(bond al2 h42)
(bond al2 h43)
(bond al2 h44)
(bond li2 al2)
(bond h41 al2)
(bond h42 al2)
(bond h43 al2)
(bond h44 al2)
; third LiAlH4
(bond al3 li3)
(bond al3 h45)
(bond al3 h46)
(bond al3 h47)
(bond al3 h48)
(bond li3 al3)
(bond h45 al3)
(bond h46 al3)
(bond h47 al3)
(bond h48 al3)
; fourth LiAlH4
(bond al4 li4)
(bond al4 h49)
(bond al4 h50)
(bond al4 h51)
(bond al4 h52)
(bond li4 al4)
(bond h49 al4)
(bond h50 al4)
(bond h51 al4)
(bond h52 al4)
; first BnBr 
(bond br1 c18)
(bond c18 br1)
(bond c18 c19)
(bond c19 c18)
(doublebond c19 c20)
(doublebond c20 c19)
(bond c20 c21)
(bond c21 c20)
(doublebond c21 c22)
(doublebond c22 c21)
(bond c22 c23)
(bond c23 c22)
(doublebond c23 c24)
(doublebond c24 c23)
(bond c19 c24)
(bond c24 c19)
(bond c18 h17)
(bond h17 c18)
(bond c18 h18)
(bond h18 c18)
(bond c20 h19)
(bond h19 c20)
(bond c21 h20)
(bond h20 c21)
(bond c22 h21)
(bond h21 c22)
(bond c23 h22)
(bond h22 c23)
(bond c24 h23)
(bond h23 c24)
; second BnBr 
(bond br2 c25)
(bond c25 br2)
(bond c25 c26)
(bond c26 c25)
(doublebond c26 c27)
(doublebond c27 c26)
(bond c27 c28)
(bond c28 c27)
(doublebond c28 c29)
(doublebond c29 c28)
(bond c29 c30)
(bond c30 c29)
(doublebond c30 c31)
(doublebond c31 c30)
(bond c26 c31)
(bond c31 c26)
(bond c25 h24)
(bond h24 c25)
(bond c25 h25)
(bond h25 c25)
(bond c27 h26)
(bond h26 c27)
(bond c28 h27)
(bond h27 c28)
(bond c29 h28)
(bond h28 c29)
(bond c30 h29)
(bond h29 c30)
(bond c31 h30)
(bond h30 c31)
; third BnBr 
(bond br3 c32)
(bond c32 br3)
(bond c32 c33)
(bond c33 c32)
(doublebond c33 c34)
(doublebond c34 c33)
(bond c34 c35)
(bond c35 c34)
(doublebond c35 c36)
(doublebond c36 c35)
(bond c36 c37)
(bond c37 c36)
(doublebond c37 c38)
(doublebond c38 c37)
(bond c33 c38)
(bond c38 c33)
(bond c32 h53)
(bond h53 c32)
(bond c32 h54)
(bond h54 c32)
(bond c34 h55)
(bond h55 c34)
(bond c35 h56)
(bond h56 c35)
(bond c36 h57)
(bond h57 c36)
(bond c37 h58)
(bond h58 c37)
(bond c38 h59)
(bond h59 c38)
; fourth BnBr 
(bond br4 c39)
(bond c39 br4)
(bond c39 c40)
(bond c40 c39)
(doublebond c40 c41)
(doublebond c41 c40)
(bond c41 c42)
(bond c42 c41)
(doublebond c42 c43)
(doublebond c43 c42)
(bond c43 c44)
(bond c44 c43)
(doublebond c44 c45)
(doublebond c45 c44)
(bond c40 c45)
(bond c45 c40)
(bond c39 h60)
(bond h60 c39)
(bond c39 h61)
(bond h61 c39)
(bond c41 h62)
(bond h62 c41)
(bond c42 h63)
(bond h63 c42)
(bond c43 h64)
(bond h64 c43)
(bond c44 h65)
(bond h65 c44)
(bond c45 h66)
(bond h66 c45)
)
(:goal
(and
bond(c3,o1,S)
bond(o1,c18,S)
bond(c18,c19,S)
doubleBond(c19,c20,S)
bond(c20,c21,S)
doubleBond(c21,c22,S)
bond(c22,c23,S)
doubleBond(c23,c24,S)
bond(c19,c24,S)
bond(c3,c1,S)
bond(c1,c2,S)
bond(c2,c4,S)
bond(c4,o3,S)
bond(o3,c25,S)
bond(c25,c26,S)
doubleBond(c26,c27,S)
bond(c27,c28,S)
doubleBond(c28,c29,S)
bond(c29,c30,S)
doubleBond(c30,c31,S)
bond(c26,c31,S)
bond(c2,c17,S)
bond(c17,c16,S)
bond(c16,o7,S)
bond(o7,c39,S)
bond(c39,c40,S)
doubleBond(c40,c41,S)
bond(c41,c42,S)
doubleBond(c42,c43,S)
bond(c43,c44,S)
doubleBond(c44,c45,S)
bond(c40,c45,S)
bond(c17,c13,S)
bond(c13,c12,S)
bond(c12,o4,S)
bond(o4,c11,S)
bond(c11,c5,S)
doubleBond(c5,c10,S)
bond(c10,c9,S)
doubleBond(c9,c8,S)
bond(c8,c7,S)
doubleBond(c7,c6,S)
bond(c5,c6,S)
bond(c13,c14,S)
bond(c1,c14,S)
bond(c14,c15,S)
bond(c15,o6,S)
bond(o6,c32,S)
bond(c32,c33,S)
doubleBond(c33,c34,S)
bond(c34,c35,S)
doubleBond(c35,c36,S)
bond(c36,c37,S)
doubleBond(c37,c38,S)
bond(c33,c38,S)
bond(c3,h46,S)
bond(c3,h47,S)
bond(c18,h17,S)
bond(c18,h18,S)
bond(c20,h19,S)
bond(c21,h20,S)
bond(c22,h21,S)
bond(c23,h22,S)
bond(c24,h23,S)
bond(c1,h1,S)
bond(c2,h2,S)
bond(c4,h50,S)
bond(c4,h51,S)
bond(c25,h24,S)
bond(c25,h25,S)
bond(c27,h26,S)
bond(c28,h27,S)
bond(c29,h28,S)
bond(c30,h29,S)
bond(c31,h30,S)
bond(c17,h16,S)
bond(c16,h15,S)
bond(c16,h41,S)
bond(c39,h60,S)
bond(c39,h61,S)
bond(c41,h62,S)
bond(c42,h63,S)
bond(c43,h64,S)
bond(c44,h65,S)
bond(c45,h66,S)
bond(c13,h12,S)
bond(c12,h10,S)
bond(c12,h11,S)
bond(c11,h8,S)
bond(c11,h9,S)
bond(c10,h7,S)
bond(c9,h6,S)
bond(c8,h5,S)
bond(c7,h4,S)
bond(c6,h3,S)
bond(c14,h13,S)
bond(c15,h14,S)
bond(c15,h37,S)
bond(c32,h53,S)
bond(c32,h54,S)
bond(c34,h55,S)
bond(c35,h56,S)
bond(c36,h57,S)
bond(c37,h58,S)
bond(c38,h59,S)
)
)
)