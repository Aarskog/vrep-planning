(define (domain robot-to-door)
		(:requirements :strips)
    (:predicates
			(at ?obj ?waypoint)
			(robot ?robot)
			(obstacle ?obstacle)
			(waypoint ?waypoint)
			(handempty)
			(moveable ?obj)
			(can-move ?from ?to)
			(clear ?waypoint)
			(holding ?robot ?obj)
    )

    (:action move
        :parameters
            (?robot
             ?from-waypoint
             ?to-waypoint)

        :precondition
            (and
                (robot ?robot)
                (waypoint ?from-waypoint)
                (waypoint ?to-waypoint)
                (at ?robot ?from-waypoint)
                (can-move ?from-waypoint ?to-waypoint)
								(clear ?to-waypoint)
								)

        :effect
            (and
                (at ?robot ?to-waypoint)
                (not (at ?robot ?from-waypoint)))
    )

		(:action pickup
				:parameters
						(?robot
						 ?obstacle
						 ?rob-pos
						 ?obstacle-pos)

				:precondition
						(and
								(robot ?robot)
								(at ?robot ?rob-pos)
								(at ?obstacle ?obstacle-pos)
								(obstacle ?obstacle)
								(can-move ?obstacle-pos ?rob-pos)
								(moveable ?obstacle)
								(handempty)
								)

				:effect
						(and
						(clear ?obstacle-pos)
						(holding ?robot ?obstacle)
						(at ?robot ?obstacle-pos)
						(not (at ?robot ?rob-pos))
						(not (at ?obstacle ?obstacle-pos))
						(not(handempty))
								)
		)

		(:action put-down
				:parameters
						(?robot
						 ?obstacle
						 ?rob-pos
						 ?put-pos)

				:precondition
						(and
								(robot ?robot)
								(at ?robot ?rob-pos)
								(obstacle ?obstacle)
								(can-move ?put-pos ?rob-pos)
								(moveable ?obstacle)
								(clear ?put-pos)
								(holding ?robot ?obstacle)
								)

				:effect
						(and
								(at ?obstacle ?put-pos)
								(handempty)
								(not (clear ?put-pos))
								(not (holding ?robot ?obstacle))
								))
		)
