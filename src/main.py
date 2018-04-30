import vrep
import rospy
from std_msgs.msg import String

class vrep_planning:
	def __init__(self):
		self.message_received = False
		self.talker()


	def callback(self,data):
		rospy.loginfo(rospy.get_name()+"I heard %s",data.data)
		if data.data == 'msg_received':
			self.message_received = True


	def talker(self):
		# rospy.init_node('listener', anonymous=True)
		rospy.Subscriber("confirm", String, self.callback)


		pub = rospy.Publisher('chatter', String, queue_size=10)
		rospy.init_node('talker', anonymous=True)
		rate = rospy.Rate(10) # 10hz
		# while not rospy.is_shutdown():
		#     hello_str = "hello world %s" % rospy.get_time()
		#     rospy.loginfo(hello_str)
		#     pub.publish(hello_str)
		#     rate.sleep()
		# for i in range(0,3):
		# 	if not rospy.is_shutdown():
		# 		hello_str = 'pickup red box'
		# 		rospy.loginfo(hello_str)
		# 		pub.publish(hello_str)
		# 		rate.sleep()

		# while not rospy.is_shutdown():
		#     hello_str = "hells world %s" % rospy.get_time()
		#     rospy.loginfo(hello_str)
		#     pub.publish(hello_str)
		#     rate.sleep()
		while not self.message_received and not rospy.is_shutdown() :
		    hello_str = "hells world %s" % rospy.get_time()
		    rospy.loginfo(hello_str)
		    pub.publish(hello_str)
		    rate.sleep()
def main():
	try:
		vp = vrep_planning()
		#talker()
	except rospy.ROSInterruptException:
		pass
if __name__=="__main__":
	main()
'''
-- This script controls the Youbot task. It is threaded. In next sections, there are a lot of function definitions
-- that ease the control of the robot. The arm of the robot is controlled in:
--
-- 1. Forward kinematics mode ( setFkMode() )
-- 2. Inverse kinematics mode in position only ( setIkMode(false) )
-- 3. Inverse kinematics mode in position and orientation (to keep the gripper vertical) ( setIkMode(true) )
--
-- The inverse kinematics calculations are then automatically applied to the physics engine, since the joints are in
-- "hybrid IK mode" (see the joint properties dialog)
--
-- All inverse kinematics tasks are define in the IK properties dialog. There are 4 tasks:
--
-- "youBotUndamped_group": handles the inverse kinematics in position only. Resolution is not damped
-- "youBotDamped_group": handles the inverse kinematics in position only. Resolution is damped. Useful when the previous IK task didn't succeed, because out of reach for instance
-- "youBotUndamped_group": handles the inverse kinematics in position and orientation. Resolution is not damped
-- "youBotDamped_group": handles the inverse kinematics in position and orientation. Resolution is damped. Useful when the previous IK task didn't succeed, because out of reach for instance
--
-- Above 4 tasks are enabled/disabled as needed. This is done with the "sim.setExplicitHandling" function.

setIkMode=function(withOrientation)
    sim.setThreadAutomaticSwitch(false) -- Don't get interrupted for this function
    if (ikMode==false) then
        sim.setObjectPosition(gripperTarget,-1,sim.getObjectPosition(gripperTip,-1))
    end
    if (withOrientation) then
        sim.setExplicitHandling(ikWithOrientation1,0)
        sim.setExplicitHandling(ikWithOrientation2,0)
    else
        sim.setExplicitHandling(ik1,0)
        sim.setExplicitHandling(ik2,0)
    end
    for i=1,5,1 do
        sim.setJointMode(armJoints[i],sim.jointmode_ik,1)
    end
    ikMode=true
    sim.setThreadAutomaticSwitch(true)
end

setFkMode=function()
    sim.setThreadAutomaticSwitch(false) -- Don't get interrupted for this function
    sim.setExplicitHandling(ik1,1)
    sim.setExplicitHandling(ik2,1)
    sim.setExplicitHandling(ikWithOrientation1,1)
    sim.setExplicitHandling(ikWithOrientation2,1)

    for i=1,5,1 do
        sim.setJointMode(armJoints[i],sim.jointmode_force,0)
    end
    ikMode=false
    sim.setThreadAutomaticSwitch(true)
end

openGripper=function()
    sim.tubeWrite(gripperCommunicationTube,sim.packInt32Table({1}))
    sim.wait(0.8)
end

closeGripper=function()
    sim.tubeWrite(gripperCommunicationTube,sim.packInt32Table({0}))
    sim.wait(0.8)
end

setGripperTargetMovingWithVehicle=function()
    sim.setObjectParent(gripperTarget,vehicleReference,true)
end

setGripperTargetFixedToWorld=function()
    sim.setObjectParent(gripperTarget,-1,true)
end

waitToReachVehicleTargetPositionAndOrientation=function()
    repeat
        sim.switchThread() -- don't waste your time waiting!
        p1=sim.getObjectPosition(vehicleTarget,-1)
        p2=sim.getObjectPosition(vehicleReference,-1)
        p={p2[1]-p1[1],p2[2]-p1[2]}
        pError=math.sqrt(p[1]*p[1]+p[2]*p[2])
        oError=math.abs(sim.getObjectOrientation(vehicleReference,vehicleTarget)[3])
    until (pError<0.001)and(oError<0.1*math.pi/180)
end

getBoxAdjustedMatrixAndFacingAngle=function(boxHandle)
    p2=sim.getObjectPosition(boxHandle,-1)
    p1=sim.getObjectPosition(vehicleReference,-1)
    p={p2[1]-p1[1],p2[2]-p1[2],p2[3]-p1[3]}
    pl=math.sqrt(p[1]*p[1]+p[2]*p[2]+p[3]*p[3])
    p[1]=p[1]/pl
    p[2]=p[2]/pl
    p[3]=p[3]/pl
    m=sim.getObjectMatrix(boxHandle,-1)
    matchingScore=0
    for i=1,3,1 do
        v={m[0+i],m[4+i],m[8+i]}
        score=v[1]*p[1]+v[2]*p[2]+v[3]*p[3]
        if (math.abs(score)>matchingScore) then
            s=1
            if (score<0) then s=-1 end
            matchingScore=math.abs(score)
            bestMatch={v[1]*s,v[2]*s,v[3]*s}
        end
    end
    angle=math.atan2(bestMatch[2],bestMatch[1])
    m=sim.buildMatrix(p2,{0,0,angle})
    return m, angle-math.pi/2
end

pickupBoxFromPlace=function(boxHandle,pickupConf)
    local m,angle=getBoxAdjustedMatrixAndFacingAngle(boxHandle)
    sim.setObjectPosition(vehicleTarget,-1,{m[4]-m[1]*dist1,m[8]-m[5]*dist1,0})
    sim.setObjectOrientation(vehicleTarget,-1,{0,0,angle})
    setFkMode()
    sim.rmlMoveToJointPositions(armJoints,-1,nil,nil,fkSpeed,fkAccel,fkJerk,pickupConf,nil)
    waitToReachVehicleTargetPositionAndOrientation()
    setIkMode(true)
    setGripperTargetFixedToWorld()
    local p=sim.getObjectPosition(gripperTarget,-1)
    p[1]=m[4]
    p[2]=m[8]
    sim.rmlMoveToPosition(gripperTarget,-1,-1,nil,nil,ikSpeed,ikAccel,ikJerk,p,nil,nil)
    openGripper()
    p[3]=m[12]
    sim.rmlMoveToPosition(gripperTarget,-1,-1,nil,nil,ikSpeed,ikAccel,ikJerk,p,nil,nil)
    closeGripper()
    p[3]=p[3]+0.1
    sim.rmlMoveToPosition(gripperTarget,-1,-1,nil,nil,ikSpeed,ikAccel,ikJerk,p,nil,nil)
    setGripperTargetMovingWithVehicle()
    setFkMode()
end

dropToPlatform=function(platform)
    setFkMode()
    sim.rmlMoveToJointPositions(armJoints,-1,nil,nil,fkSpeed,{0.3,0.3,0.3,0.3,0.3},fkJerk,platform,nil)
    openGripper()
end

pickupFromPlatformAndReorient=function(boxHandle)
    setFkMode()
    sim.rmlMoveToJointPositions(armJoints,-1,nil,nil,fkSpeed,fkAccel,fkJerk,platformIntermediateDrop,nil)
    setIkMode(false)
    local p=sim.getObjectPosition(boxHandle,-1)
    sim.rmlMoveToPosition(gripperTarget,-1,-1,nil,nil,ikSpeed,ikAccel,ikJerk,p,nil,nil)
    closeGripper()
    setFkMode()
    -- Move a bit back from current position:
    local m=sim.getObjectMatrix(vehicleTarget,-1)
    sim.setObjectPosition(vehicleTarget,-1,{m[4]-m[2]*dist1,m[8]-m[6]*dist1,0})
    -- Now drop it
    sim.rmlMoveToJointPositions(armJoints,-1,nil,nil,fkSpeed,fkAccel,fkJerk,pickup2,nil)
    openGripper()
    sim.wait(1)
    -- Now orient yourself according to the box and pick it up:
    local m,angle=getBoxAdjustedMatrixAndFacingAngle(boxHandle)
    sim.setObjectPosition(vehicleTarget,-1,{m[4]-m[1]*dist1,m[8]-m[5]*dist1,0})
    sim.setObjectOrientation(vehicleTarget,-1,{0,0,angle})
    waitToReachVehicleTargetPositionAndOrientation()
    sim.rmlMoveToJointPositions(armJoints,-1,nil,nil,fkSpeed,fkAccel,fkJerk,pickup2,nil)
    setIkMode(true)
    setGripperTargetFixedToWorld()
    local p=sim.getObjectPosition(gripperTarget,-1)
    p[1]=m[4]
    p[2]=m[8]
    sim.rmlMoveToPosition(gripperTarget,-1,-1,nil,nil,ikSpeed,ikAccel,ikJerk,p,nil,nil)
    p[3]=0.03
    sim.rmlMoveToPosition(gripperTarget,-1,-1,nil,nil,ikSpeed,ikAccel,ikJerk,p,nil,nil)
    closeGripper()
    p[3]=p[3]+0.1
    sim.rmlMoveToPosition(gripperTarget,-1,-1,nil,nil,ikSpeed,ikAccel,ikJerk,p,nil,nil)
    setGripperTargetMovingWithVehicle()
    setFkMode()
end

dropToPlace=function(placeHandle,shift,verticalPos,startConf,noVerticalArmForUpMovement)
    local m,angle=getBoxAdjustedMatrixAndFacingAngle(placeHandle)
    m[4]=m[4]+m[2]*shift
    m[8]=m[8]+m[6]*shift
    sim.setObjectPosition(vehicleTarget,-1,{m[4]-m[1]*dist1,m[8]-m[5]*dist1,0})
    sim.setObjectOrientation(vehicleTarget,-1,{0,0,angle})
    setFkMode()
    sim.rmlMoveToJointPositions(armJoints,-1,nil,nil,fkSpeed,fkAccel,fkJerk,startConf,nil)
    waitToReachVehicleTargetPositionAndOrientation()
    setIkMode(true)
    setGripperTargetFixedToWorld()
    local p=sim.getObjectPosition(gripperTarget,-1)
    p[1]=m[4]
    p[2]=m[8]
    sim.rmlMoveToPosition(gripperTarget,-1,-1,nil,nil,ikSpeed,ikAccel,ikJerk,p,nil,nil)
    p[3]=verticalPos
    sim.rmlMoveToPosition(gripperTarget,-1,-1,nil,nil,ikSpeed,ikAccel,ikJerk,p,nil,nil)
    openGripper()
    if (noVerticalArmForUpMovement) then
        setIkMode(false)
    end
    p[3]=p[3]+0.1
    sim.rmlMoveToPosition(gripperTarget,-1,-1,nil,nil,ikSpeed,ikAccel,ikJerk,p,nil,nil)
    setGripperTargetMovingWithVehicle()
    setFkMode()
end

function subscriber_callback(msg)
    -- This is the subscriber callback function
    sim.addStatusbarMessage('subscriber receiver following String: '..msg.data)
    simROS.publish(publisher,{data='msg_received'})
    if not doing then
        run_thing()
        doing = true
    end

end









function sysCall_threadmain()
    doing = false

    -- Check if the required RosInterface is there:
    moduleName=0
    index=0
    rosInterfacePresent=false
    while moduleName do
        moduleName=sim.getModuleName(index)
        if (moduleName=='RosInterface') then
            rosInterfacePresent=true
        end
        index=index+1
    end

    -- Prepare the float32 publisher and subscriber (we subscribe to the topic we advertise):
    if rosInterfacePresent then
        publisher=simROS.advertise('/confirm','std_msgs/String')
        subscriber=simROS.subscribe('/chatter','std_msgs/String','subscriber_callback')
    end

    --run_thing()
    while (true) do
        a = 1
    end

end


function run_thing()
    gripperTarget=sim.getObjectHandle('youBot_gripperPositionTarget')
    gripperTip=sim.getObjectHandle('youBot_gripperPositionTip')
    vehicleReference=sim.getObjectHandle('youBot_vehicleReference')
    vehicleTarget=sim.getObjectHandle('youBot_vehicleTargetPosition')
    redBox1=sim.getObjectHandle('redRectangle1')
    yellowBox1=sim.getObjectHandle('yellowRectangle1')
    yellowBox2=sim.getObjectHandle('yellowRectangle2')
    greenBox1=sim.getObjectHandle('greenRectangle1')
    greenBox2=sim.getObjectHandle('greenRectangle2')
    greenBox3=sim.getObjectHandle('greenRectangle3')
    armJoints={-1,-1,-1,-1,-1}
    for i=0,4,1 do
        armJoints[i+1]=sim.getObjectHandle('youBotArmJoint'..i)
    end
    ik1=sim.getIkGroupHandle('youBotUndamped_group')
    ik2=sim.getIkGroupHandle('youBotDamped_group')
    ikWithOrientation1=sim.getIkGroupHandle('youBotPosAndOrientUndamped_group')
    ikWithOrientation2=sim.getIkGroupHandle('youBotPosAndOrientDamped_group')
    gripperCommunicationTube=sim.tubeOpen(0,'youBotGripperState'..sim.getNameSuffix(nil),1)
    place1=sim.getObjectHandle('place1')
    place2=sim.getObjectHandle('place2')
    place3=sim.getObjectHandle('place3')

    pickup1={0,-14.52*math.pi/180,-70.27*math.pi/180,-95.27*math.pi/180,0*math.pi/180}
    pickup2={0,-13.39*math.pi/180,-93.91*math.pi/180,-72.72*math.pi/180,90*math.pi/180}
    pickup3={0,-14.52*math.pi/180,-70.27*math.pi/180,-95.27*math.pi/180,90*math.pi/180}
    platformIntermediateDrop={0,16*math.pi/180,52*math.pi/180,73*math.pi/180,0*math.pi/180}
    platformDrop1={0,54.33*math.pi/180,32.88*math.pi/180,35.76*math.pi/180,0*math.pi/180}--{0,-0.4,0.2}
    platformDrop2={0,40.74*math.pi/180,45.81*math.pi/180,59.24*math.pi/180,0*math.pi/180}--{0,-0.32,0.2}
    platformDrop3={0,28.47*math.pi/180,55.09*math.pi/180,78.32*math.pi/180,0*math.pi/180}--{0,-0.24,0.2}

    dist1=0.2
    dropHeight1=0.035
    dropHeight2=0.095
    dropHeight3=0.155
    ikSpeed={0.2,0.2,0.2,0.2}
    ikAccel={0.1,0.1,0.1,0.1}
    ikJerk={0.1,0.1,0.1,0.1}
    fkSpeed={1,1,1,1,1}
    fkAccel={0.6,0.6,0.6,0.6,0.6}
    fkJerk={1,1,1,1,1}


    setGripperTargetMovingWithVehicle()
    setFkMode()
    openGripper()


    -- redBox first pickup:
    m,angle=getBoxAdjustedMatrixAndFacingAngle(redBox1)
    sim.setObjectPosition(vehicleTarget,-1,{m[4]-m[1]*dist1,m[8]-m[5]*dist1,0})
    sim.setObjectOrientation(vehicleTarget,-1,{0,0,angle})
    sim.setFloatSignal('cameraJoint',-159*math.pi/180)
    waitToReachVehicleTargetPositionAndOrientation()
    sim.rmlMoveToJointPositions(armJoints,-1,nil,nil,fkSpeed,fkAccel,fkJerk,pickup1,nil)
    setIkMode(true)
    p=sim.getObjectPosition(gripperTarget,-1)
    p[1]=m[4]
    p[2]=m[8]
    p[3]=m[12]
    sim.rmlMoveToPosition(gripperTarget,-1,-1,nil,nil,ikSpeed,ikAccel,ikJerk,p,nil,nil)
    closeGripper()
    p[3]=p[3]+0.05
    sim.rmlMoveToPosition(gripperTarget,-1,-1,nil,nil,ikSpeed,ikAccel,ikJerk,p,nil,nil)
end
function rest()
    -- redBox first drop:
    dropToPlace(place3,0,dropHeight1,pickup2,false)
    -- yellow box1 first pickup and intermediate drop:
    pickupBoxFromPlace(yellowBox1,pickup2)
    -- yellow box1 intermediate drop onto platform:
    dropToPlatform(platformDrop2)
    sim.setFloatSignal('cameraJoint',20*math.pi/180)

    --yellow box2 first pickup:
    pickupBoxFromPlace(yellowBox2,pickup2)
    -- yellow box2 first drop:
    dropToPlace(place2,0.04,dropHeight1,pickup2,false)
    pickupFromPlatformAndReorient(yellowBox1)
    dropToPlace(place2,-0.04,dropHeight1,pickup2,false)


    pickupBoxFromPlace(redBox1,pickup2)
    dropToPlace(place2,0,dropHeight2,pickup2,false)

    sim.setFloatSignal('cameraJoint',-50*math.pi/180)

    pickupBoxFromPlace(greenBox1,pickup2)
    sim.setInt32Parameter(sim.intparam_current_page,4)
    dropToPlatform(platformDrop1)
    pickupBoxFromPlace(greenBox2,pickup2)
    dropToPlatform(platformDrop3)
    pickupBoxFromPlace(greenBox3,pickup2)
    sim.setFloatSignal('cameraJoint',80*math.pi/180)
    dropToPlace(place3,0.08,dropHeight1,pickup2,false)
    sim.setInt32Parameter(sim.intparam_current_page,0)
    pickupFromPlatformAndReorient(greenBox2)
    dropToPlace(place3,0.0,dropHeight1,pickup2,false)
    pickupFromPlatformAndReorient(greenBox1)
    dropToPlace(place3,-0.08,dropHeight1,pickup2,false)


    pickupBoxFromPlace(redBox1,pickup2)
    dropToPlace(place1,0,dropHeight1,pickup2,false)


    pickupBoxFromPlace(yellowBox1,pickup2)
    dropToPlatform(platformDrop2)
    pickupBoxFromPlace(yellowBox2,pickup2)
    dropToPlace(place3,0.04,dropHeight2,pickup2,false)
    pickupFromPlatformAndReorient(yellowBox1)

    setFkMode()
    sim.rmlMoveToJointPositions(armJoints,-1,nil,nil,fkSpeed,fkAccel,fkJerk,pickup3,nil)
    dropToPlace(place3,-0.04,dropHeight2,pickup3,true)


    pickupBoxFromPlace(redBox1,pickup1)


    dropToPlace(place3,0,dropHeight3,pickup1,true)


    sim.setObjectPosition(vehicleTarget,-1,{0,0,0})
    sim.wait(2)
    sim.setObjectOrientation(vehicleTarget,-1,{0,0,0})
    setFkMode()
    sim.rmlMoveToJointPositions(armJoints,-1,nil,nil,fkSpeed,fkAccel,fkJerk,platformIntermediateDrop,nil)
    waitToReachVehicleTargetPositionAndOrientation()
    sim.stopSimulation()
end
'''
