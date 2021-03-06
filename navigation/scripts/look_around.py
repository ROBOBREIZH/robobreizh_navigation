#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rosgraph.names import is_private
import rospy
from naoqi_bridge_msgs.msg import JointAnglesWithSpeed 
def move_head():
	pub = rospy.Publisher('/joint_angles', JointAnglesWithSpeed, queue_size=10)
	rospy.init_node('move_head', anonymous=True)
	rate = rospy.Rate(4)

	head_pitch = 0.15
	head_yaw = 0.00
	incr_pitch = 0.10
	incr_yaw = 0.05
	count_back_and_forth = 0
	is_positif = True
	while not rospy.is_shutdown() and count_back_and_forth < 4:
		# [HeadPitch, HeadYaw]
		# HeadPitch [-0.71, 0.64]
		# HeadYaw [-2.09,2.09]
		msg = create_msg([head_pitch,head_yaw])

		pub.publish(msg)

		if is_positif:
			head_yaw += incr_yaw
			if(head_yaw+incr_yaw > 2.09):	
				is_positif = False
				head_pitch+=incr_pitch
				count_back_and_forth+=1
		else:
			head_yaw -= incr_yaw
			if(head_yaw-incr_yaw < -2.09):
				is_positif = True
				head_pitch+=incr_pitch
				count_back_and_forth+=1

		rate.sleep()

	#put pepper's head straight
	msg = create_msg([0.15,0.00])
	pub.publish(msg)

# format data to trajectory_msgs format
def create_msg(positions):
	trajectory = JointAnglesWithSpeed() 
	trajectory.header.stamp = rospy.Time.now()
	trajectory.header.frame_id = "";

	trajectory.joint_names.append("HeadPitch");
	trajectory.joint_names.append("HeadYaw");

	trajectory.joint_angles = positions
	trajectory.speed = 0.1
	trajectory.relative = 0

	return trajectory

if __name__=='__main__':
    try:
        move_head()
    except rospy.ROSInterruptException:
        pass