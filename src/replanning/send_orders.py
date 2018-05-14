import rospy
import numpy as np
from std_msgs.msg import String
import replanning.youbot_replanning as yr
from solver import PDDLparser as pp
import os

class replan_send:
	def __init__(self,plan,path,domain=None):
		self.domain = domain
		self.path = path
		self.realplan = []
		self.replanning = False
		self.plan = self.generate_plan(plan)
		self.talker(domain)

	def generate_plan(self,plan):
		stacks = {}

		vrep_coord_map = adjust_to_vrep_coordinates(0.5,(5,5))
		actions = []
		for action in plan:
			self.realplan.append(action)
			action = action.split()
			if action[0] == 'move':
				to_waypoint = action[3]
				two_d  = one_d_two_d(to_waypoint[8:])
				two_d = vrep_coord_map[str(two_d)]
				actions.append('move '+str(two_d[0])+' '+str(two_d[1]))


			elif action[0] == 'pickup':
				actions.append('pickup '+action[2].lower())
				to_waypoint = action[4]
				two_d  = one_d_two_d(to_waypoint[8:])
				two_d = vrep_coord_map[str(two_d)]
				actions.append('move '+str(two_d[0])+' '+str(two_d[1]))
				self.realplan.append('move ROBOT ' + action[-2] + ' ' + action[-1])

			elif action[0] == 'put-down':
				to_waypoint = action[4]
				from_waypoint = action[3]
				to2d = one_d_two_d(to_waypoint[8:])
				to2d = vrep_coord_map[str(to2d)]

				from2d = one_d_two_d(from_waypoint[8:])
				from2d = vrep_coord_map[str(from2d)]
				actions.append('put-down '+str(to2d[0])+' '+str(to2d[1]))




		actions.append('end')
		self.realplan.append('end')
		return actions

	def callback(self,data):


		if data.data == 'msg_received':
			self.plan.pop(0)
		elif data.data == 'new_boxes_spawned':

			self.replanning = True
			domain =self.domain
			obstacles = domain.obstacle_objects
			new_obstacles = [yr.Obstacle((4,3),'b1'),yr.Obstacle((3,3),'b2'),\
				yr.Obstacle((3,4),'b3')]
			obstacles.extend(new_obstacles)


			dir_path = os.path.dirname(os.path.realpath(__file__))
			dir_path = dir_path[:-3]


			domain = yr.youbot_replan(domain.world_size,domain.robot.pos,domain.goal,obstacles=obstacles,path=self.path[1])
			# solver = 'bFS'
			solver = None
			# solver = 'missing state'


			solv = pp.Solver(self.path[0],self.path[1],solver,print_progress = True,debug = False, profiling = False)
			solution = solv.get_solution()
			self.plan = self.generate_plan(solution)
			self.talker(domain)


	def talker(self,domain):
		# rospy.init_node('listener', anonymous=True)
		rospy.Subscriber("confirm", String, self.callback)


		pub = rospy.Publisher('chatter', String, queue_size=10)
		rospy.init_node('talker', anonymous=True)
		rate = rospy.Rate(10) # 10hz

		prev_msg = ''
		while not rospy.is_shutdown() and self.plan:
			# str = "hells world %s" % rospy.get_time()
			msg = self.plan[0]
			if not msg==prev_msg:

				rospy.loginfo('ROS message sent: '+msg)
				domain.do_action(self.realplan.pop(0))
				print '\n'
				prev_msg = msg
			if not self.replanning:
				pub.publish(msg)
			rate.sleep()



def one_d_two_d(num):
	'''
	1 dim to 2 dims
	'''
	num = int(num)
	return (num/5,num%5)

def adjust_to_vrep_coordinates(dist,size):
	#size = (5,5)
	vrep_coord_map = np.zeros((size[0],size[1]))
	vrep_coord_map = {}
	#print vrep_coord_map[0]
	for i in range(0,size[0]):
		for j in range(0,size[1]):
			vrep_coord_map[str((i,j))] = (int((size[0]-dist-2*dist*i)*2),int((size[1]-dist-2*dist*j)*2))
	return vrep_coord_map
