import vrep
import rospy
from std_msgs.msg import String
import PDDLparser
import towerOfHanoiPDDL as toh
import os
import PDDLparser as pp
'''
Actions:
pickupBoxFromPlace(box,where)
dropToPlace(where to place,place left right or middle,what height level,initial pos)
dropToPlatform(where to drop on platform)
pickupFromPlatformAndReorient (box)
'''

class vrep_youbot_planning:
	def __init__(self):

		self.message_received = False
		self.plan = \
		[["pickupBoxFromPlace redBox1 pickup1"],		["dropToPlace place3 middle dropHeight1 pickup1"],\
		["pickupBoxFromPlace yellowBox1 pickup2"],		['dropToPlatform platformDrop2'],\
		["pickupBoxFromPlace yellowBox2 pickup2"],		["dropToPlace place2 right dropHeight1 pickup2"],\
		['pickupFromPlatformAndReorient yellowBox1'],	["dropToPlace place2 left dropHeight1 pickup2"],\
		["pickupBoxFromPlace redBox1 pickup2"],			["dropToPlace place2 middle dropHeight2 pickup2"],\
		['pickupBoxFromPlace greenBox1 pickup2'],		['dropToPlatform platformDrop1'],\
		['pickupBoxFromPlace greenBox2 pickup2'],		['dropToPlatform platformDrop3'],\
		['pickupBoxFromPlace greenBox3 pickup2'],		['dropToPlace place3 rightmost dropHeight1 pickup2'],\
		['pickupFromPlatformAndReorient greenBox2'],	['dropToPlace place3 middle dropHeight1 pickup2'],\
		['pickupFromPlatformAndReorient greenBox1'],	['dropToPlace place3 leftmost dropHeight1 pickup2'],\
		['pickupBoxFromPlace redBox1 pickup2'],			['dropToPlace place1 middle dropHeight1 pickup2'],\
		['pickupBoxFromPlace yellowBox1 pickup2'],		['dropToPlatform platformDrop2'],\
		['pickupBoxFromPlace yellowBox2 pickup2'],		['dropToPlace place3 right dropHeight2 pickup2'],\
		['pickupFromPlatformAndReorient yellowBox1'],	['dropToPlace place3 left dropHeight2 pickup3'],\
		['pickupBoxFromPlace redBox1 pickup1'],			['dropToPlace place3 middle dropHeight3 pickup1'],['end']]

		self.talker()

	def generate_hanoi_plan(self,plan):

		#Name map of
		name_map = {}

		for action in plan:
			action = action.split()
			print action



	def callback(self,data):
		# rospy.loginfo(rospy.get_name()+"I heard %s",data.data)
		rospy.loginfo('Action complete')
		if data.data == 'msg_received':
			self.plan.pop(0)
			#self.message_received = True

	def talker(self):
		# rospy.init_node('listener', anonymous=True)
		rospy.Subscriber("confirm", String, self.callback)


		pub = rospy.Publisher('chatter', String, queue_size=10)
		rospy.init_node('talker', anonymous=True)
		rate = rospy.Rate(10) # 10hz

		prev_msg = ''
		while not rospy.is_shutdown() and self.plan:
			# str = "hells world %s" % rospy.get_time()
			msg = self.plan[0][0]
			if not msg==prev_msg:
				rospy.loginfo(msg)
				prev_msg = msg
			pub.publish(msg)
			rate.sleep()

def main():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	dir_path = dir_path[:-3]

	# define paths
	problem_file_name = dir_path+'pddl/youbothanoi/problem.pddl'
	domain_file_name = dir_path+'pddl/youbothanoi/domain.pddl'
	# #


	try:
		#--------------Generate solution--------------
		# solver = 'bFS'
		# # solver = None
		# # solver = 'missing state'
		#
		# towh = toh.Tower_of_hanoi(3,problem_file_name)
		# solv = pp.Solver(domain_file_name,problem_file_name,solver,print_progress = False,debug = False, profiling = False)
		# # solv.print_solution()


		#--------------------------------------------

		vp = vrep_youbot_planning()
		# vp.generate_plan(solv.get_solution())


	except rospy.ROSInterruptException:
		pass



if __name__=="__main__":
	main()
