(define (domain hanoi)
  (:requirements :strips)
  (:predicates (disk ?disk)
							(table ?table)
							(smaller ?x ?y)
							(on ?disk ?x)
  )

  (:action move
     :parameters (?disk ?from ?to)
     :precondition (and (on ?disk ?from) (clear ?disk) (clear ?to) (smaller ?disk ?to))
     :effect (and (not (clear ?to)) (not (on ?disk ?from))
		 (clear ?from) (on ?disk ?to)
		 )))
