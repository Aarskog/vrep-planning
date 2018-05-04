(define (problem blocks)
(:domain BLOCKS)
(:objects
	r1 r2
	r3 y1
	y2 y3
	ground1 ground2
	height1 height2 height3
	height4 height5 height6
	platform1 platform2 platform3
)
(:init
(on r3 y2) (on y1 y3)
(on r1 r3) (on r2 y1)
(on y2 ground1) (on y3 ground2)

(clear r1) (clear r2)

(moveable r1) (moveable r2)
(moveable r3) (moveable y1)
(moveable y2) (moveable y3)

(height height1) (height height2) (height height3)
(height height4) (height height5) (height height6)
(height height00) (height height01)

(at height1 y2) (at height2 r3) (at height3 r1)
(at height4 y3) (at height5 y1) (at height6 r2)
(at height00 ground1) (at height01 ground2)

(above height2 height1) (above height3 height2) (above height1 height00)
(above height5 height4) (above height6 height5) (above height4 height01)

(platform platform1) (platform platform2) (platform platform3)
(clear platform1) (clear platform2) (clear platform3)

(handempty)

)
(:goal (and
(on r3 ground1) (on y3 ground2)
(on r2 r3) (on y2 y3)
(on r1 r2) (on y1 y2)
)))
