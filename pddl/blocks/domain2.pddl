(define (domain BLOCKS)
  (:requirements :strips)
  (:predicates (on ?x ?y)
	       (onplatform ?x ?platform)
				 (platform ?platform)
				 (height ?height)
	       (clear ?x)
	       (handempty)
	       (holding ?x)
				 (at ?x ?stack)
				 (moveable ?x)
				 (above ?heightx ?heighty)
				 )

  (:action pick-up-from-platform
	     :parameters (?x ?platform)
	     :precondition (and (onplatform ?x ?platform) (handempty) (platform ?platform))
	     :effect
	     (and (not (onplatform ?x ?platform))
		   (not (handempty))
		   (holding ?x)
			 (clear ?platform)))

  (:action put-on-platform
	     :parameters (?x ?platform)
	     :precondition (and (holding ?x) (platform ?platform) (clear ?platform))
	     :effect
	     (and (not (holding ?x))
		   (not (clear ?platform))
		   (handempty)
		   (onplatform ?x ?platform)))


  (:action stack
	     :parameters (?x ?y ?heightx ?heighty)
	     :precondition (and (moveable ?x) (height ?heightx) (height ?heighty)
			 (above ?heightx ?heighty) (at ?heighty ?y) (clear ?y) (clear ?heightx) (holding ?x))
	     :effect
			 (and (not (holding ?x))
			(not (clear ?y))
			(not (clear ?heightx))
			(clear ?x)
			(at ?heightx ?x)
			(handempty)
			(on ?x ?y)))

  (:action unstack
	     :parameters (?x ?y ?height)
	     :precondition (and (on ?x ?y) (clear ?x) (handempty) (height ?height)
			 (moveable ?x) (at ?height ?x))
	     :effect
	     (and (holding ?x)
		   (clear ?y)
			 (clear ?height)
			 (not (at ?height ?x))
		   (not (clear ?x))
		   (not (handempty))
		   (not (on ?x ?y)))))
