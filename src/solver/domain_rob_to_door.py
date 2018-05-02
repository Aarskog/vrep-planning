import numpy as np
import os
import math
import sys

class Domain_rob_to_door:
	def __init__(self,world_size,robot_start,door_pos,obstacles=None,path=None):
		#Make room
		self.room = [["   " for x in range(world_size[1])] for y in range(world_size[0])]
		self.room_size = world_size
		self.obstacles={}
		for obstacle in obstacles:
			self.room[obstacle.pos[0]][obstacle.pos[1]] = obstacle.name

			self.obstacles[(obstacle.pos[0],obstacle.pos[1])] = obstacle
		self.obstacles_array = obstacles

		self.robot = Robot(robot_start)

		#Set robot position
		self.room[robot_start[0]][robot_start[1]] = self.robot.name
		self.robot.pos = robot_start

		#Set door position
		self.room[door_pos[0]][door_pos[1]] = ' D '
		self.door_pos = door_pos

		#Make each tile to waypoints and the adjacency matrix
		self.waypoints = []
		self.adjacency_waypoints = self.create_adjacency(world_size,self.waypoints)


		self.path = path
		self.make_pddl_problem(robot_start,door_pos,obstacles,world_size,path)

	def create_adjacency(self,world_size,waypoints):
		adjacency_waypoints = np.zeros((world_size[0]*world_size[1],world_size[0]*world_size[1]))
		k = 0
		i = 0
		for row in self.room:
			j = 0
			for tile in row:
				waypoints.append('waypoint' + str(k))

				#Move up or down
				if k-world_size[1]>=0:
					adjacency_waypoints[k][k-world_size[1]] = 1
					adjacency_waypoints[k-world_size[1]][k] = 1

				if j == 0:
					adjacency_waypoints[k][k+1] = 1
					adjacency_waypoints[k+1][k] = 1

				elif j == (world_size[1]-1):
					adjacency_waypoints[k][k-1] = 1
					adjacency_waypoints[k-1][k] = 1

				else:
					adjacency_waypoints[k][k-1] = 1
					adjacency_waypoints[k-1][k] = 1
					adjacency_waypoints[k][k+1] = 1
					adjacency_waypoints[k+1][k] = 1

				k = k + 1
				j = j + 1
			i = i + 1
		return adjacency_waypoints

	def print_room(self):
		for tiles in self.get_room():
			print tiles
			#print repr([x.encode(sys.stdout.encoding) for x in tiles]).decode('string-escape')

	def get_room(self):
		return self.room

	def make_pddl_problem(self,robot_start,door_pos,obstacles,world_size,path):
		adjacencies = self.get_adjacencies()

		#Lines contains the lines which are written to the pddl file
		lines = []

		lines.append('(define (problem rtd)')
		lines.append('(:domain robot-to-door)')

		#------------------objects--------------------------------
		lines.append('(:objects')
		lines.append('robot')
		lines.append('door')

		for waypoint in self.waypoints:
			lines.append(waypoint)

		obstacle_num = 1
		for obstacle in obstacles:
			lines.append('obstacle'+str(obstacle_num))
			obstacle_num += 1

		lines.append(')')
		#------------------------------------------------------------


		#-------------------Initial state ----------------------
		lines.append('(:init')
		lines.append('(robot robot)')
		lines.append('(door door)')
		lines.append('(handempty)')
		lines.append('(at robot waypoint' + str(world_size[1]*self.robot.pos[0]+self.robot.pos[1]) +  ')')


		for waypoint in self.waypoints:
			lines.append('(waypoint '+waypoint+')')
			lines.append('(clear '+ waypoint+')')

		for adjacency in adjacencies:
			lines.append('(can-move '+adjacency[0]+' '+adjacency[1]+')')

		obstacle_num = 1
		for obstacle in obstacles:
			obstacle_name = 'obstacle'+str(obstacle_num)

			obstacle_pos = 'waypoint' + str(world_size[1]*obstacle.pos[0]+obstacle.pos[1])

			lines.append('(obstacle ' + obstacle_name+')')

			if obstacle.moveable:
				lines.append('(moveable '+ obstacle_name+')')

			lines.append('(at '+ obstacle_name + ' ' + obstacle_pos+')')
			#print 'clear '+obstacle_pos
			lines.remove('(clear '+obstacle_pos+')')

			obstacle_num += 1


		lines.append(')')




		#--------------------------------------------------------


		#-----------------------Goal----------------------------------
		lines.append('(:goal (and')
		lines.append('(at robot waypoint'+str(world_size[1]*door_pos[0]+door_pos[1])+')')
		lines.append('(handempty)')

		lines.append(')))')
		#-------------------------------------------------------------------

		self.make_pddl_file(lines,path)

	def make_pddl_file(self,lines,path):
		with open(path, 'w') as the_file:
			for line in lines:
				the_file.write(line+'\n')

	def get_adjacencies(self):
		adjacencies = []
		i = 0
		for row in self.adjacency_waypoints:
			j = 0
			for item in row:
				if item:
					adjacencies.append(['waypoint'+str(i),'waypoint'+str(j)])
				j = j + 1
			i = i + 1
		return adjacencies

	def do_action(self,action):
		'''
			Updates the visualization of the domain
		'''
		success = True

		spl_act = action.split()
		#print spl_act
		if spl_act[0] == 'move':

			#To waypoint
			to_wp = spl_act[-1]
			new_pos = (int(to_wp[8:])/self.room_size[1],int(to_wp[8:])%self.room_size[1])

			self.room[self.robot.pos[0]][self.robot.pos[1]] = "   "
			#self.room[new_pos[0]][new_pos[1]] = self.robot

			self.robot.pos=new_pos




		elif spl_act[0] == 'pickup':

			obstacle_pos = spl_act[-1]
			obstacle_pos = (int(obstacle_pos[8:])/self.room_size[1],int(obstacle_pos[8:])%self.room_size[1])
			obstacle = self.obstacles[obstacle_pos]
			#removekey(self.obstacles,obstacle_pos)


			self.room[obstacle_pos[0]][obstacle_pos[1]] = "   "
			#self.room[self.robot.pos[0]][self.robot.pos[1]] = self.robot

			obstacle.discovered = True

			obstacle.update_obstacle()
			if obstacle.moveable:
				self.robot.holding = obstacle
				self.robot.name = " rO"
				removekey(self.obstacles,obstacle_pos)
			else:

				self.room[obstacle_pos[0]][obstacle_pos[1]] = obstacle.name
				self.make_pddl_problem( self.robot.pos,self.door_pos,self.obstacles_array,self.room_size,self.path)

				success = False


		elif spl_act[0] == 'put-down':
			self.robot.name = " r "
			obstacle_pos = spl_act[-1]
			obstacle_pos = (int(obstacle_pos[8:])/self.room_size[1],int(obstacle_pos[8:])%self.room_size[1])
			self.obstacles[obstacle_pos] = self.robot.holding
			self.robot.holding.pos = obstacle_pos

			self.room[obstacle_pos[0]][obstacle_pos[1]] = " O "

			self.robot.holding = None

		self.room[self.robot.pos[0]][self.robot.pos[1]] = self.robot.name
		print action
		self.print_room()
		#print '\n'
		return success
			#print to_wp[8:],int(to_wp[8:])/self.room_size[1],int(to_wp[8:])%self.room_size[1]


class Obstacle:
	def __init__(self,pos,moveable=True):
		self.pos = pos
		self.moveable = moveable
		self.discovered = False
		if moveable:
			self.name = ' O '
		else:
			self.name = ' | '

	def update_obstacle(self):
		one=1


class Obstacle_hidden(Obstacle):
	def __init__(self,pos,moveable=True):

		Obstacle.__init__(self,pos,moveable=True)

		#self.pos = pos
		#self.moveable = True
		self.name = ' O '
		self.moveable_after_discovery = moveable
		#self.discovered = False

	def update_obstacle(self):
		if self.discovered and not self.moveable_after_discovery:
			self.name = ' | '
			self.moveable = False


		# if moveable:
		# 	self.name = ' O '
		# else:
		# 	self.name = ' | '#u"\u2588"


class Robot:
	def __init__(self,pos):
		self.name=' r '
		self.pos = pos

		#Holding object
		self.holding = None


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def one_d_2_2d(d1):
	'''1D coord to 2D coord'''

#
# def main():
# 	dir_path = os.path.dirname(os.path.realpath(__file__))
# 	dir_path = dir_path[:-3]
#
# 	path = dir_path+'probs/robot_to_door/problem.pddl'
#
# 	world_size = (7,7)
# 	rob_pos = (0,0)
# 	door_pos = (6,6)
#
# 	dom24 = Domain_rob_to_door(world_size,rob_pos,door_pos,path=path)
# 	dom24.print_room()
#
# if __name__=='__main__':
# 	main()
