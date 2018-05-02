import rospy
import Hanoi.towerOfHanoiPDDL as toh
import os
from solver import PDDLparser as pp
import vrep_youbot as vy




def main():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	dir_path = dir_path[:-3]

	# define paths
	problem_file_name = dir_path+'pddl/youbothanoi/problem.pddl'
	domain_file_name = dir_path+'pddl/youbothanoi/domain.pddl'
	# #


	try:
		#--------------Generate solution--------------
		solver = 'bFS'
		# solver = None
		# solver = 'missing state'

		towh = toh.Tower_of_hanoi(3,problem_file_name)
		solv = pp.Solver(domain_file_name,problem_file_name,solver,print_progress = False,debug = False, profiling = False)
		# solv.print_solution()


		#--------------------------------------------

		vp = vy.vrep_youbot_planning(solv.get_solution())



	except rospy.ROSInterruptException:
		pass



if __name__=="__main__":
	main()
