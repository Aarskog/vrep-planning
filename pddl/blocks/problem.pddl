(define (problem blocks)
(:domain BLOCKS)
(:objects
	r1 r2 r3
	y1 y2 y3
	g1 g2 g3
	unm1 unm2 unm3
	height1 height2 height3
	height4 height5 height6
	height7 height8 height9
	platform1 platform2 platform3
	stack1 stack2 stack3
)
(:init
(on g1 unm1) (on g2 unm2) (on g3 unm3)
(on y1 g1) (on y2 g2) (on y3 g3)
(on r1 y1) (on r2 y2) (on r3 y3)

(clear r1) (clear r2) (clear r3)

(moveable r1) (moveable r2) (moveable r3)
(moveable y1) (moveable y2) (moveable y3)
(moveable g1) (moveable g2) (moveable g3)
(moveable unm1) (moveable unm2) (moveable unm3)

(height height1) (height height2) (height height3)
(height height4) (height height5) (height height6)
(height height7) (height height8) (height height9)

(at height1 g1) (at height2 y1) (at height3 r1)
(at height4 g2) (at height5 y2) (at height6 r2)
(at height7 g3) (at height8 y3) (at height9 r3)

(at height1 stack1) (at height2 stack1) (at height3 stack1)
(at height4 stack2) (at height5 stack2) (at height6 stack2)
(at height7 stack3) (at height8 stack3) (at height9 stack3)



(platform platform1) (platform platform2) (platform platform3)
(clear platform1) (clear platform2) (clear platform3)

(stack stack1) (stack stack2) (stack stack3)

(handempty)

)
(:goal (and
(on g1 unm1) (on g2 unm2) (on g3 unm3)
(on y1 g1) (on y2 g2) (on y3 g3)
(on r2 y1) (on y2 r1) (on r3 y3)
)))
