import rospy
import Hanoi.towerOfHanoiPDDL as toh
import os
from solver import PDDLparser as pp
import Hanoi.vrep_youbot as vy
import blocks.blocksSendOrders as bs
import replanning.youbot_replanning as yr
import replanning.send_orders as so


def tower_of_hanoi():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	dir_path = dir_path[:-3]

	# define paths
	problem_file_name = dir_path+'pddl/youbothanoi/problem.pddl'
	domain_file_name = dir_path+'pddl/youbothanoi/domain.pddl'
	# #


	try:
		#--------------Generate solution--------------
		# solver = 'bFS'
		solver = None
		# solver = 'missing state'

		towh = toh.Tower_of_hanoi(3,problem_file_name)
		solv = pp.Solver(domain_file_name,problem_file_name,solver,print_progress = True,debug = False, profiling = False)
		# solv.print_solution()


		#--------------------------------------------

		vp = vy.vrep_youbot_planning(solv.get_solution())



	except rospy.ROSInterruptException:
		pass

def blocks():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	dir_path = dir_path[:-3]

	# define paths
	problem_file_name = dir_path+'pddl/blocks/problem2.pddl'
	domain_file_name = dir_path+'pddl/blocks/domain2.pddl'
	# #


	try:
		#--------------Generate solution--------------
		solver = 'bFS'
		# solver = None
		# solver = 'missing state'

		solv = pp.Solver(domain_file_name,problem_file_name,solver,print_progress = True,debug = True, profiling = False)
		# solv.print_solution()


		#--------------------------------------------

		vp = bs.blocks_send(solv.get_solution())



	except rospy.ROSInterruptException:
		pass

def blocks_3_stacks():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	dir_path = dir_path[:-3]

	# define paths
	problem_file_name = dir_path+'pddl/blocks/problem3stacks.pddl'
	domain_file_name = dir_path+'pddl/blocks/domain2.pddl'
	# #


	try:
		#--------------Generate solution--------------
		# solver = 'bFS'
		# solver = None
		solver = 'missing state'

		solv = pp.Solver(domain_file_name,problem_file_name,solver,print_progress = True,debug = True, profiling = False)
		# solv.print_solution()


		#--------------------------------------------

		vp = bs.blocks_send_3_stacks(solv.get_solution())



	except rospy.ROSInterruptException:
		pass

def youbot_replanning():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	dir_path = dir_path[:-3]

	# define paths
	problem_file_name = dir_path+'pddl/youbotreplan/problem.pddl'
	domain_file_name = dir_path+'pddl/youbotreplan/domain.pddl'
	# #

	world_size = (5,5)
	robot_start = (4,4)
	goal = ['(at robot waypoint24)','(holding robot r1)']
	obstacles = [yr.Obstacle((0,0),'r1'),yr.Obstacle((0,1),'g1'),\
	yr.Obstacle((1,1),'g2'),yr.Obstacle((1,0),'g3')]
	yr.youbot_replan(world_size,robot_start,goal,obstacles=obstacles,path=problem_file_name)


	# solver = 'bFS'
	# solver = None
	solver = 'missing state'

	solv = pp.Solver(domain_file_name,problem_file_name,solver,print_progress = True,debug = True, profiling = False)
	# solv.print_solution()
	try:
		so.replan_send(solv.get_solution())
	except rospy.ROSInterruptException:
		pass

def main():
	youbot_replanning()

if __name__=="__main__":
	main()
