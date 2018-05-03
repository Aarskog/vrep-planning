import domain as dom
import state as st
import os
from heapq import heappush
from heapq import heappop
import time
import domain_rob_to_door as drtd

class Solver:
	def __init__(self,domain_path,problem_path,solver,print_progress=True,debug = False,profiling=False):
		# debug = False
		debug = debug
		profiling = profiling

		domain_file = open(domain_path,'r')
		problem_file = open(problem_path,'r')

		#dom24.print_room()


		try:
			domain = dom.Domain(domain_file)
			init_state = st.State(domainclass = domain,problem_file=problem_file)

			start_time = time.time()

			if debug:
				self.debug(domain,init_state)

			if profiling:
				pr = cProfile.Profile()
				pr.enable()

			#Solve the problem
			self.solution = self.solve(init_state,solver,print_progress)


			if profiling:
				pr.disable()
				s = StringIO.StringIO()
				sortby = 'cumulative'
				ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
				ps.print_stats()
				print s.getvalue()

			if print_progress:
				print("--- %s seconds ---" % (time.time() - start_time))



		except ValueError as err:
			print '------------------'
			for arg in err.args:
				print arg
			print '------------------'

	def solve(self,initial_state,solver=None,print_progress=True):

		heap = []

		heappush(heap,initial_state)
		visited_states = {tuple(initial_state.state):True}

		i = 0
		new_states_inserted = 0
		lowest_dist = float('inf')
		deepest = 0


		while heap:# and i < 1000 :

			#Get the state with the lowest cost from the heap
			possible_solution = heappop(heap)

			if possible_solution.estimated_dist_to_goal < lowest_dist:
				lowest_dist = possible_solution.estimated_dist_to_goal
			if possible_solution.depth > deepest:
				deepest = possible_solution.depth

			if print_progress:
				print 'Visited:',i,' len queue:',len(heap),' depth:',possible_solution.depth,deepest,\
			' New states:',new_states_inserted,' State cost: ',possible_solution.cost,\
			' Dist goal: ',possible_solution.estimated_dist_to_goal,lowest_dist#,len(possible_solution.state)

			if possible_solution.is_goal_state():
				if print_progress:
					print '\n\n----------Solution found!---------------\n'
					#print 'The state is:\n',possible_solution.state
					print '\n\nThe goal was:'
					for goal in possible_solution.goal: print goal
					print '\nLength of solution: ',len(possible_solution.actions)
					print '\nThe solution is: '
					for action in possible_solution.actions:
						print action
					print '\n\n'
				return possible_solution.actions


			else:
				possible_solution.create_child_states()
				new_states = possible_solution.get_child_states()
				new_states_inserted = 0
				for new_state in new_states:

					#check if the state already has been visited using hash table
					if not tuple(new_state.state) in visited_states:
						# print '\n'
						# print '---',new_state.parent_action.name,'---',new_state.action_parameters
						# print '\n'
						new_state.set_state_cost(solver)
						#Add the new state to visited states
						visited_states[tuple(new_state.state)] = True
						new_states_inserted = new_states_inserted + 1

						#Add the new state to the queue using a heap sorted based on
						#the state cost
						heappush(heap,new_state)


			# possible_solution.missing_goal_states_heuristic()
			# print '\n'
			# for s in possible_solution.state:
			# 	print s
			i = i + 1


		print '---NOT SOLVABLE---'
		print 'Nodes visited = ',i

	def debug(self,domain,init_state):
		print "\n\nDomain name: ",domain.domain_name
		for predicate in domain.predicates:
			print "Predicate: ",predicate.name,predicate.parameters

		for action in domain.actions:
			print "\n\nAction name:",action.name
			print "Parameters:", action.parameters
			for precondition in action.preconditions:
				print "Precondition: ",precondition.name,precondition.parameters

			for effect in action.effects:
				print "Effect: ",effect.name, effect.parameters
			for delete_effect in action.delete_effects:
				print "Delete effect: ",delete_effect.name,delete_effect.parameters


		print '\n----------Objects-----------------'
		for obj in init_state.objects:
			print obj
		print '\n-------INIT STATE-----------'
		for state in init_state.state:
			print state

		print '\n-------Goal-----------'
		for goal in init_state.goal:
			print goal

	def get_solution(self):
		return self.solution

	def print_solution(self):
		solution = self.get_solution()
		print 'Length of solution: ',len(solution),'\n'
		for action in solution:
			print action
def main():

	dir_path = os.path.dirname(os.path.realpath(__file__))
	dir_path = dir_path[:-3]



	#Make robot to door problem
	rob2door = False
	if rob2door:
		path = dir_path+'probs/robot_to_door/problem.pddl'

		world_size = (4,5)
		rob_pos = (0,0)
		door_pos = (world_size[0]-1,world_size[1]-1)
		obstacles = [drtd.Obstacle((2,0)),drtd.Obstacle((1,0)),drtd.Obstacle((3,0)),\
		drtd.Obstacle_hidden((0,1),False),drtd.Obstacle_hidden((1,1),False),drtd.Obstacle_hidden((2,1),False),drtd.Obstacle((3,1)),\
		drtd.Obstacle((0,2)),drtd.Obstacle((1,2)),drtd.Obstacle((2,2)),drtd.Obstacle((3,2)),
		drtd.Obstacle((0,3)),drtd.Obstacle_hidden((1,3),False),drtd.Obstacle_hidden((2,3),False),drtd.Obstacle_hidden((3,3),False)]

		dom24 = drtd.Domain_rob_to_door(world_size,rob_pos,door_pos,path=path,obstacles=obstacles)


	# # # # # robot to door
	# problem_file_name = dir_path+'probs/robot_to_door/problem.pddl'
	# domain_file_name = dir_path+'probs/robot_to_door/domain.pddl'
	# # #

	# satellite problem.
	# domain_file_name = dir_path+'probs/satellite/domain.pddl'
	# problem_file_name = dir_path+'probs/satellite/problem01.pddl'
	# # # # # # #
	# #
	# # #Block world
	problem_file_name = dir_path+'probs/blocks/problem.pddl'
	domain_file_name = dir_path+'probs/blocks/domain.pddl'
	# #

	# # # #aircargo problem
	# problem_file_name = dir_path+'probs/aircargo/problem.pddl'
	# domain_file_name = dir_path+'probs/aircargo/domain.pddl'


	# # # # Shakey
	# problem_file_name = dir_path+'probs/shakey/problem1.pddl'
	# domain_file_name = dir_path+'probs/shakey/domain.pddl'
	# #

 	# # # # # #Rover1
	# problem_file_name = dir_path+'probs/rover/problem.pddl'
	# domain_file_name = dir_path+'probs/rover/domain.pddl'


 	# # # # # # #Rover2
	# problem_file_name = dir_path+'probs/rover2/problem.pddl'
	# domain_file_name = dir_path+'probs/rover2/domain.pddl'


 	solv = Solver(domain_file_name,problem_file_name)
	solution = solv.get_solution()



	#Execute plan for robot to door
	if rob2door:
		print '\nInitial state'
		dom24.print_room()
		print '\n'

		i = 0
		while solution:
			action = solution.pop(0)
			print '\n'

			if not dom24.do_action(action):
				#domain_file = open(domain_file_name,'r')
				#problem_file = open(problem_file_name,'r')
				#init_state = st.State(domainclass = domain,problem_file=problem_file)

				print 'Can not pick up. Replanning'
				solv = Solver(domain_file_name,problem_file_name,print_progress=False)
				solution = solv.get_solution()
				#i = i - 1
			i = i + 1
		print i,' actions attempted'



if __name__=='__main__':
	main()

#https://github.com/primaryobjects/strips/tree/master/strips
#Fix naar action bare har en effect. Det blir rart
