(define (problem blocks)
(:domain BLOCKS)
(:objects
	r1 r2 r3
	y1 y2 y3
	g1 g2 g3
	ground1 ground2 ground3
	height1 height2 height3
	height4 height5 height6
	height7 height8 height9
	platform1 platform2
)
(:init
(on g1 ground1) (on g2 ground2) (on g3 ground3)
(on y1 g1) (on y2 g2) (on y3 g3)
(on r1 y1) (on r2 y2) (on r3 y3)

(clear r1) (clear r2) (clear r3)

(moveable r1) (moveable r2)
(moveable r3) (moveable y1)
(moveable y2) (moveable y3)
(moveable g1) (moveable g2)
(moveable g3)

(height height1) (height height2) (height height3)
(height height4) (height height5) (height height6)
(height height7) (height height8) (height height9)
(height height00) (height height01) (height height02)

(at height1 g1) (at height2 y1) (at height3 r1)
(at height4 g2) (at height5 y2) (at height6 r2)
(at height7 g3) (at height8 y3) (at height9 r3)
(at height00 ground1) (at height01 ground2) (at height02 ground3)

(above height2 height1) (above height3 height2) (above height1 height00)
(above height5 height4) (above height6 height5) (above height4 height01)
(above height8 height7) (above height9 height8) (above height7 height02)

(platform platform1) (platform platform2) (platform platform3)
(clear platform1) (clear platform2) (clear platform3)

(handempty)

)
(:goal (and
(on r1 ground1) (on y1 ground2) (on g1 ground3)
(on r2 r1) (on y2 y1) (on g2 g1)
(on r3 r2) (on y3 y2) (on g3 g2)
)))
