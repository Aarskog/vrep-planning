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

		self.stack = {}
		self.stack['height00'] = 'stack1'
		self.stack['height1'] = 'stack1'
		self.stack['height2'] = 'stack1'
		self.stack['height3'] = 'stack1'
		self.stack['height4'] = 'stack2'
		self.stack['height5'] = 'stack2'
		self.stack['height6'] = 'stack2'
		self.stack['height01'] = 'stack2'


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
				actions.append(['dropToPlace '+'place1 '+self.stack[action[4].lower()]+' '+self.heights[action[3].lower()]+' pickup1'])

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


class blocks_send_3_stacks:
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
		self.heights['height7'] = 'dropHeight1'
		self.heights['height8'] = 'dropHeight2'
		self.heights['height9'] = 'dropHeight3'

		self.platforms = {}
		self.platforms['PLATFORM1'] = 'platformDrop1'
		self.platforms['PLATFORM2'] = 'platformDrop2'
		self.platforms['PLATFORM3'] = 'platformDrop3'

		self.stack = {}
		self.stack['height00'] = 'stack1'
		self.stack['height01'] = 'stack2'
		self.stack['height02'] = 'stack3'
		self.stack['height1'] = 'stack1'
		self.stack['height2'] = 'stack1'
		self.stack['height3'] = 'stack1'
		self.stack['height4'] = 'stack2'
		self.stack['height5'] = 'stack2'
		self.stack['height6'] = 'stack2'
		self.stack['height7'] = 'stack3'
		self.stack['height8'] = 'stack3'
		self.stack['height9'] = 'stack3'


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
				actions.append(['dropToPlace '+'place1 '+self.stack[action[4].lower()]+' '+self.heights[action[3].lower()]+' pickup1'])

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
		i = 1
		while not rospy.is_shutdown() and self.plan:
			# str = "hells world %s" % rospy.get_time()
			msg = self.plan[0][0]
			if not msg==prev_msg:
				rospy.loginfo(str(i)+'\t'+msg)
				i = i + 1
				prev_msg = msg
			pub.publish(msg)
			rate.sleep()
