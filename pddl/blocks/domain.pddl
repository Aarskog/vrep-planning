(define (domain BLOCKS)
  (:requirements :strips)
  (:predicates (on ?x ?y)
	       (onplatform ?x ?platform)
				 (platform ?platform)
				 (height ?height)
	       (clear ?x)
	       (handempty)
	       (holding ?x)
				 (stack ?stack)
				 (at ?x ?stack)
				 (moveable ?x)
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
	     :parameters (?x ?y ?height ?stack ?heightplace)
	     :precondition (and (holding ?x) (clear ?y) (height ?height) (height ?heightplace) (stack ?stack)
			 (clear ?height) (at ?height ?stack) (at ?heightplace ?stack) (at ?heightplace ?y) (moveable ?x) (moveable ?y))
	     :effect
	     (and (not (holding ?x))
		   (not (clear ?y))
			 (not (clear ?height))
		   (clear ?x)
			 (at ?height ?x)
		   (handempty)
		   (on ?x ?y)))

  (:action unstack
	     :parameters (?x ?y ?height ?stack)
	     :precondition (and (on ?x ?y) (clear ?x) (handempty) (height ?height) (stack ?stack) (at ?height ?stack)
			 (moveable ?x) (moveable ?y) (at ?height ?x))
	     :effect
	     (and (holding ?x)
		   (clear ?y)
			 (clear ?height)
			 (not (at ?height ?x))
		   (not (clear ?x))
		   (not (handempty))
		   (not (on ?x ?y)))))
