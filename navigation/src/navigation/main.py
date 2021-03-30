#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalID
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import quaternion_from_euler
import numpy as np
from threading import Thread
from threading import Event
from Queue import Queue
from navigation.msg import CurrentPos

import math 
import time

class Navigation :

	pepperPosition = []
	finish = False

	# def __init__(self) :
	# 	pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size = 10)
	# 	checkpoint = PoseWithCovarianceStamped()
		 
	# 	checkpoint.pose.pose.position.x = 0.8331
	# 	checkpoint.pose.pose.position.y = 0.6744
	# 	checkpoint.pose.pose.position.z = 0.0
		
	# 	checkpoint.pose.pose.orientation.x = 0.0
	# 	checkpoint.pose.pose.orientation.y = 0.0
	# 	checkpoint.pose.pose.orientation.z = -0.336
	# 	checkpoint.pose.pose.orientation.w = 0.941
		 
	# 	alpha = self.quaternion_to_euler(checkpoint.pose.pose.orientation.x, checkpoint.pose.pose.orientation.y, checkpoint.pose.pose.orientation.z, checkpoint.pose.pose.orientation.w)
	# 	print checkpoint
	# 	pub.publish(checkpoint)
	# 	self.pepperPosition = [checkpoint.pose.pose.position.x, checkpoint.pose.pose.position.y, alpha[0]]

	# 	Thread(target=self.updatePos).start()
	# 	Thread(target=self.publishPos).start()
		
	def LocalizationPepper():
		return 0

	def ObjectPersonLocalization():
		return 0

	def PersonFollowing():
		return 0

	def updatePos(self):
		rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, self.callbackNewPos)
		rospy.spin()

	def publishPos(self):
		pub = rospy.Publisher('/currentPos', CurrentPos, queue_size=10)
		rate = rospy.Rate(10) # 10hz
		while not rospy.is_shutdown():
			msg = CurrentPos()
			msg.posX = np.float32(self.pepperPosition[0])
			msg.posY = np.float32(self.pepperPosition[1])
			msg.alpha = np.float32(self.pepperPosition[2])
			pub.publish(msg)
			rate.sleep()

	def euler_to_quaternion(self, roll, pitch, yaw):

		qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
		qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
		qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
		qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

		return [qx, qy, qz, qw]


	def quaternion_to_euler(self, x, y, z, w):

		t0 = +2.0 * (w * x + y * z)
		t1 = +1.0 - 2.0 * (x * x + y * y)
		roll = math.atan2(t0, t1)
		t2 = +2.0 * (w * y - z * x)
		t2 = +1.0 if t2 > +1.0 else t2
		t2 = -1.0 if t2 < -1.0 else t2
		pitch = math.asin(t2)
		t3 = +2.0 * (w * z + x * y)
		t4 = +1.0 - 2.0 * (y * y + z * z)
		yaw = math.atan2(t3, t4)

		return [yaw, pitch, roll]

	def init_pose(self, pose):
		pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size = 10)
		rospy.sleep(2)
		checkpoint = PoseWithCovarianceStamped()
		 
		#POSE 1 :
		# X = 4.95
		# Y = 0.65
		# qz = 0.858509857791
		# qw = 0.512797059348


		#POSE 2 :
		# X = 2.80
		# Y = 0.74
		# qz = 0.858509857791
		# qw = 0.512797059348
		
		if pose == "POSE1":

			checkpoint.pose.pose.position.x = 4.95
			checkpoint.pose.pose.position.y = 0.65
			checkpoint.pose.pose.position.z = 0.0
			
			checkpoint.pose.pose.orientation.x = 0.0
			checkpoint.pose.pose.orientation.y = 0.0
			checkpoint.pose.pose.orientation.z = 0.711777083929
			checkpoint.pose.pose.orientation.w = 0.702405426227

		if pose == "POSE2":

			checkpoint.pose.pose.position.x = 2.80
			checkpoint.pose.pose.position.y = 0.74
			checkpoint.pose.pose.position.z = 0.0
			
			checkpoint.pose.pose.orientation.x = 0.0
			checkpoint.pose.pose.orientation.y = 0.0
			checkpoint.pose.pose.orientation.z = 0.858509857791
			checkpoint.pose.pose.orientation.w = 0.512797059348

		alpha = self.quaternion_to_euler(checkpoint.pose.pose.orientation.x, checkpoint.pose.pose.orientation.y, checkpoint.pose.pose.orientation.z, checkpoint.pose.pose.orientation.w)
		print checkpoint
		pub.publish(checkpoint)
		self.pepperPosition = [checkpoint.pose.pose.position.x, checkpoint.pose.pose.position.y, alpha[0]]

		Thread(target=self.updatePos).start()
		Thread(target=self.publishPos).start()
		return self.pepperPosition

	#New
	def getPepperPose(self):
		"""
		Description:
			Returns initials Pepper's coordinates in the environment coordinate system.
		Parameters:
			None
		Returns:
			(float) coord_X_init: Initial Pepper's X coordinate in the environment coordinate system.
			(float) coord_Y_init: Initial Pepper's X coordinate in the environment coordinate system.
			(float) theta_init: Initial Pepper's angle in the environment coordinate system.
		"""
		angle = self.quaternion_to_euler(0.0,0.0,0.858509857791,0.512797059348)

		return 2.80, 0.74, angle[0]

	def callbackNewPos(self,msg):
		alpha = self.quaternion_to_euler(msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w)
		self.pepperPosition = [msg.pose.pose.position.x, msg.pose.pose.position.y, alpha[0]]

	def drive(self, coord_x, coord_y, theta):
		theta = theta * 3.14 / 180
		pose=rospy.wait_for_message("/currentPos", CurrentPos) 
		thetaDest = pose.alpha - theta
		
		quater = self.euler_to_quaternion(0.0,0.0, thetaDest)
		client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		client.wait_for_server()

		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()
		goal.target_pose.pose.position.x = coord_x
		goal.target_pose.pose.position.y = coord_y
		goal.target_pose.pose.orientation.w = quater[3]
		goal.target_pose.pose.orientation.z = quater[2]

		client.send_goal(goal)
		wait = client.wait_for_result()
		if not wait:
			rospy.logerr("Action server not available!")
			rospy.signal_shutdown("Action server not available!")
		else:
			self.finish = True
			print self.finish

	def MoveToDestination(self, coord_x, coord_y, theta, timer):
		"""
		Descritpion:
			Pepper moves to the specified point (coord_X, coord_Y).
		Parameters:
			(float) coord_X: X coordinate of the target point in the environment coordinate system.
			(float) coord_Y: Y coordinate of the target point in the environment coordinate system.
			(float) theta: Angle between Pepper direction and Pepper/target axe.
		Returns:
			Nothing useful.
		"""
		theta = theta * 3.14 / 180
		pose=rospy.wait_for_message("/currentPos", CurrentPos) 
		thetaDest = pose.alpha - theta
		
		quater = self.euler_to_quaternion(0.0,0.0, thetaDest)
		client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		client.wait_for_server()

		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()
		goal.target_pose.pose.position.x = coord_x
		goal.target_pose.pose.position.y = coord_y
		goal.target_pose.pose.orientation.w = quater[3]
		goal.target_pose.pose.orientation.z = quater[2]
		
		client.send_goal(goal)
		wait = client.wait_for_result(rospy.Duration(timer))
		if (not wait):
			client.cancel_goal()

		return wait




	def getOperatorPose(self):

		#POSE 1 :
		# X = 4.95
		# Y = 0.65
		# qz = 0.858509857791
		# qw = 0.512797059348

		angle = self.quaternion_to_euler(0.0,0.0,0.711777083929,0.702405426227)
		return 4.00, 1.0, 0.0