(define (problem blocks)
(:domain BLOCKS)
(:objects
	r1 r2
	r3 y1
	y2 y3
	unm1 unm2
	height1 height2 height3
	height4 height5 height6
	height7 height8
	platform1 platform2 platform3
	stack1 stack2
)
(:init
(on y2 unm1) (on y3 unm2)
(on r3 y2) (on y1 y3)
(on r1 r3) (on r2 y1)

(clear r1) (clear r2)

(moveable r1) (moveable r2)
(moveable r3) (moveable y1)
(moveable y2) (moveable y3)
(moveable unm1) (moveable unm2)

(height height1) (height height2) (height height3)
(height height4) (height height5) (height height6)
(height height7) (height height8)

(at height1 y2) (at height2 r3) (at height3 r1)
(at height4 y3) (at height5 y1) (at height6 r2)
(at height7 unm1) (at height6 unm8)

(at height1 stack1) (at height2 stack1) (at height3 stack1)
(at height4 stack2) (at height5 stack2) (at height6 stack2)
(at height7 stack1) (at height8 stack2)



(platform platform1) (platform platform2) (platform platform3)
(clear platform1) (clear platform2) (clear platform3)

(stack stack1) (stack stack2)

(handempty)

)
(:goal (and
(on r3 unm1) (on y3 unm2)
(on r2 r3) (on y2 y3)
(on r1 r2) (on y1 y2)
)))
