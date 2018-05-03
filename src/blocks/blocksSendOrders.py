import rospy
from std_msgs.msg import String
'''
Actions:
pickupBoxFromPlace(box,where)
dropToPlace(where to place,place left right or middle,what height level,initial pos)
dropToPlatform(where to drop on platform)
pickupFromPlatformAndReorient (box)
'''

class blocks_send:
	def __init__(self,plan):

		self.message_received = False

		self.plan = []

		self.heights = {}
		self.heights['height1'] = 'dropHeight1'
		self.heights['height2'] = 'dropHeight2'
		self.heights['height3'] = 'dropHeight3'
		self.heights['height4'] = 'dropHeight1'
		self.heights['height5'] = 'dropHeight2'
		self.heights['height6'] = 'dropHeight3'

		self.platforms = {}
		self.platforms['PLATFORM1'] = 'platformDrop1'
		self.platforms['PLATFORM2'] = 'platformDrop2'
		self.platforms['PLATFORM3'] = 'platformDrop3'
		# self.name_map = {}
		# self.name_map['TABLE1'] = 'place1'
		# self.name_map['TABLE2'] = 'place2'
		# self.name_map['TABLE3'] = 'place3'
		#
		# self.name_map['DISK1'] = 'place1'
		# self.name_map['DISK2'] = 'place1'
		# self.name_map['DISK3'] = 'place1'

		self.generate_plan(plan)

		self.talker()

	def generate_plan(self,plan):
		stacks = {}


		actions = []
		for action in plan:
			action = action.split()
			if action[0] == 'unstack':
				actions.append(['pickupBoxFromPlace '+action[1].lower()+' pickup1'])
			elif action[0] == 'stack':
				dropheight =self.heights[action[3].lower()]
				actions.append(['dropToPlace '+'place1 '+action[4].lower()+' '+self.heights[action[3].lower()]+' pickup1'])

			elif action[0] == 'put-on-platform':
				actions.append(['dropToPlatform '+ self.platforms[action[2]]])

			elif action[0] == 'pick-up-from-platform':
				actions.append(['pickupFromPlatformAndReorient '+action[1].lower()])


		actions.append(['end'])
		self.plan = actions

	def callback(self,data):
		# rospy.loginfo(rospy.get_name()+"I heard %s",data.data)
		# rospy.loginfo('Action complete')
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


''' solution but wrong
The solution is:
unstack R1 R3 HEIGHT3 STACK1
put-on-platform R1 PLATFORM2
unstack R3 Y2 HEIGHT2 STACK1
put-on-platform R3 PLATFORM1
unstack Y2 UNM1 HEIGHT1 STACK1
put-on-platform Y2 PLATFORM3
pick-up-from-platform R3 PLATFORM1
stack R3 UNM1 HEIGHT3 STACK1 HEIGHT7
unstack R2 Y1 HEIGHT6 STACK2
stack R2 R3 HEIGHT2 STACK1 HEIGHT3
unstack Y1 Y3 HEIGHT5 STACK2
put-on-platform Y1 PLATFORM1
pick-up-from-platform Y2 PLATFORM3
stack Y2 Y3 HEIGHT5 STACK2 HEIGHT4
pick-up-from-platform R1 PLATFORM2
stack R1 R2 HEIGHT1 STACK1 HEIGHT2
pick-up-from-platform Y1 PLATFORM1
stack Y1 Y2 HEIGHT6 STACK2 HEIGHT5

'''
