import rospy
import numpy as np
from std_msgs.msg import String

class replan_send:
	def __init__(self,plan):

		self.plan = self.generate_plan(plan)

		self.talker()

	def generate_plan(self,plan):
		stacks = {}

		vrep_coord_map = adjust_to_vrep_coordinates(0.5,(5,5))
		actions = []
		for action in plan:
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
			elif action[0] == 'put-down':
				to_waypoint = action[4]
				from_waypoint = action[3]
				to2d = one_d_two_d(to_waypoint[8:])
				to2d = vrep_coord_map[str(to2d)]

				from2d = one_d_two_d(from_waypoint[8:])
				from2d = vrep_coord_map[str(from2d)]
				actions.append('put-down '+str(to2d[0])+' '+str(to2d[1]))
				actions.append('move '+str(from2d[0])+' '+str(from2d[1]))


		actions.append('end')
		return actions

	def callback(self,data):

		if data.data == 'msg_received':
			self.plan.pop(0)


	def talker(self):
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
				rospy.loginfo(msg)
				prev_msg = msg
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
