(define (problem rtd)
(:domain robot-to-door)
(:objects
robot
waypoint0
waypoint1
waypoint2
waypoint3
waypoint4
waypoint5
waypoint6
waypoint7
waypoint8
waypoint9
waypoint10
waypoint11
waypoint12
waypoint13
waypoint14
waypoint15
waypoint16
waypoint17
waypoint18
waypoint19
waypoint20
waypoint21
waypoint22
waypoint23
waypoint24
r1
g1
g2
g3
)
(:init
(robot robot)
(handempty)
(at robot waypoint24)
(waypoint waypoint0)
(waypoint waypoint1)
(waypoint waypoint2)
(clear waypoint2)
(waypoint waypoint3)
(clear waypoint3)
(waypoint waypoint4)
(clear waypoint4)
(waypoint waypoint5)
(waypoint waypoint6)
(waypoint waypoint7)
(clear waypoint7)
(waypoint waypoint8)
(clear waypoint8)
(waypoint waypoint9)
(clear waypoint9)
(waypoint waypoint10)
(clear waypoint10)
(waypoint waypoint11)
(clear waypoint11)
(waypoint waypoint12)
(clear waypoint12)
(waypoint waypoint13)
(clear waypoint13)
(waypoint waypoint14)
(clear waypoint14)
(waypoint waypoint15)
(clear waypoint15)
(waypoint waypoint16)
(clear waypoint16)
(waypoint waypoint17)
(clear waypoint17)
(waypoint waypoint18)
(clear waypoint18)
(waypoint waypoint19)
(clear waypoint19)
(waypoint waypoint20)
(clear waypoint20)
(waypoint waypoint21)
(clear waypoint21)
(waypoint waypoint22)
(clear waypoint22)
(waypoint waypoint23)
(clear waypoint23)
(waypoint waypoint24)
(clear waypoint24)
(can-move waypoint0 waypoint1)
(can-move waypoint0 waypoint5)
(can-move waypoint1 waypoint0)
(can-move waypoint1 waypoint2)
(can-move waypoint1 waypoint6)
(can-move waypoint2 waypoint1)
(can-move waypoint2 waypoint3)
(can-move waypoint2 waypoint7)
(can-move waypoint3 waypoint2)
(can-move waypoint3 waypoint4)
(can-move waypoint3 waypoint8)
(can-move waypoint4 waypoint3)
(can-move waypoint4 waypoint9)
(can-move waypoint5 waypoint0)
(can-move waypoint5 waypoint6)
(can-move waypoint5 waypoint10)
(can-move waypoint6 waypoint1)
(can-move waypoint6 waypoint5)
(can-move waypoint6 waypoint7)
(can-move waypoint6 waypoint11)
(can-move waypoint7 waypoint2)
(can-move waypoint7 waypoint6)
(can-move waypoint7 waypoint8)
(can-move waypoint7 waypoint12)
(can-move waypoint8 waypoint3)
(can-move waypoint8 waypoint7)
(can-move waypoint8 waypoint9)
(can-move waypoint8 waypoint13)
(can-move waypoint9 waypoint4)
(can-move waypoint9 waypoint8)
(can-move waypoint9 waypoint14)
(can-move waypoint10 waypoint5)
(can-move waypoint10 waypoint11)
(can-move waypoint10 waypoint15)
(can-move waypoint11 waypoint6)
(can-move waypoint11 waypoint10)
(can-move waypoint11 waypoint12)
(can-move waypoint11 waypoint16)
(can-move waypoint12 waypoint7)
(can-move waypoint12 waypoint11)
(can-move waypoint12 waypoint13)
(can-move waypoint12 waypoint17)
(can-move waypoint13 waypoint8)
(can-move waypoint13 waypoint12)
(can-move waypoint13 waypoint14)
(can-move waypoint13 waypoint18)
(can-move waypoint14 waypoint9)
(can-move waypoint14 waypoint13)
(can-move waypoint14 waypoint19)
(can-move waypoint15 waypoint10)
(can-move waypoint15 waypoint16)
(can-move waypoint15 waypoint20)
(can-move waypoint16 waypoint11)
(can-move waypoint16 waypoint15)
(can-move waypoint16 waypoint17)
(can-move waypoint16 waypoint21)
(can-move waypoint17 waypoint12)
(can-move waypoint17 waypoint16)
(can-move waypoint17 waypoint18)
(can-move waypoint17 waypoint22)
(can-move waypoint18 waypoint13)
(can-move waypoint18 waypoint17)
(can-move waypoint18 waypoint19)
(can-move waypoint18 waypoint23)
(can-move waypoint19 waypoint14)
(can-move waypoint19 waypoint18)
(can-move waypoint19 waypoint24)
(can-move waypoint20 waypoint15)
(can-move waypoint20 waypoint21)
(can-move waypoint21 waypoint16)
(can-move waypoint21 waypoint20)
(can-move waypoint21 waypoint22)
(can-move waypoint22 waypoint17)
(can-move waypoint22 waypoint21)
(can-move waypoint22 waypoint23)
(can-move waypoint23 waypoint18)
(can-move waypoint23 waypoint22)
(can-move waypoint23 waypoint24)
(can-move waypoint24 waypoint19)
(can-move waypoint24 waypoint23)
(obstacle r1)
(moveable r1)
(at r1 waypoint0)
(obstacle g1)
(moveable g1)
(at g1 waypoint1)
(obstacle g2)
(moveable g2)
(at g2 waypoint6)
(obstacle g3)
(moveable g3)
(at g3 waypoint5)
)
(:goal (and
(at robot waypoint24)
(holding robot r1)
)))