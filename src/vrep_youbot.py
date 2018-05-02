import rospy
from std_msgs.msg import String
'''
Actions:
pickupBoxFromPlace(box,where)
dropToPlace(where to place,place left right or middle,what height level,initial pos)
dropToPlatform(where to drop on platform)
pickupFromPlatformAndReorient (box)
'''

class vrep_youbot_planning:
	def __init__(self,plan):

		self.message_received = False

		self.plan = []

		self.heights = {}
		self.heights['place1'] = 3
		self.heights['place2'] = 0
		self.heights['place3'] = 0

		self.name_map = {}
		self.name_map['TABLE1'] = 'place1'
		self.name_map['TABLE2'] = 'place2'
		self.name_map['TABLE3'] = 'place3'

		self.name_map['DISK1'] = 'place1'
		self.name_map['DISK2'] = 'place1'
		self.name_map['DISK3'] = 'place1'

		self.generate_hanoi_plan(plan)

		self.talker()

	def generate_hanoi_plan(self,plan):

		for action in plan:
			action = action.split()

			if action[1] == 'DISK1':
				self.plan.extend(self.move_red(self.name_map[action[2]],self.name_map[action[3]]))
			elif action[1] == 'DISK2':
				self.plan.extend(self.move_yellow(self.name_map[action[2]],self.name_map[action[3]]))
			elif action[1] == 'DISK3':
				self.plan.extend(self.move_green(self.name_map[action[2]],self.name_map[action[3]]))

		self.plan.append(['end'])

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

	def move_red(self,place_from,place_to):
		self.name_map['DISK1'] = place_to
		self.heights[place_to] += 1
		self.heights[place_from] -= 1
		dropheight = 'dropHeight'+str(self.heights[place_to])
		actions = []
		actions.append(['pickupBoxFromPlace redBox1 pickup1'])
		actions.append(['dropToPlace '+place_to+' middle '+dropheight+' pickup1'])
		#["pickupBoxFromPlace redBox1 pickup1"],["dropToPlace place3 middle dropHeight1 pickup1"]

		return actions

	def move_yellow(self,place_from,place_to):
		self.name_map['DISK2'] =place_to

		self.heights[place_to] += 1
		self.heights[place_from] -= 1
		dropheight = 'dropHeight'+str(self.heights[place_to])

		actions = []
		actions.append(["pickupBoxFromPlace yellowBox1 pickup2"])
		actions.append(['dropToPlatform platformDrop2'])
		actions.append(["pickupBoxFromPlace yellowBox2 pickup2"])
		actions.append(['dropToPlace '+ place_to +' right '+dropheight+' pickup2'])
		actions.append(['pickupFromPlatformAndReorient yellowBox1'])
		actions.append(['dropToPlace '+ place_to +' left '+dropheight+' pickup2'])

		return actions

	def move_green(self,place_from,place_to):
		self.name_map['DISK3'] = place_to

		self.heights[place_to] += 1
		self.heights[place_from] -= 1
		dropheight = 'dropHeight'+str(self.heights[place_to])

		actions = []

		actions.append(['pickupBoxFromPlace greenBox1 pickup2'])
		actions.append(['dropToPlatform platformDrop1'])
		actions.append(['pickupBoxFromPlace greenBox2 pickup2'])
		actions.append(['dropToPlatform platformDrop3'])
		actions.append(['pickupBoxFromPlace greenBox3 pickup2'])
		actions.append(['dropToPlace '+ place_to +' rightmost '+dropheight+' pickup2'])
		actions.append(['pickupFromPlatformAndReorient greenBox2'])
		actions.append(['dropToPlace '+ place_to +' middle '+dropheight+' pickup2'])
		actions.append(['pickupFromPlatformAndReorient greenBox1'])
		actions.append(['dropToPlace '+ place_to +' leftmost '+dropheight+' pickup2'])

		return actions
