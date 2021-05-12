#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rosgraph.names import is_private
import rospy
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

def move_head():
	pub = rospy.Publisher('pepper/Head_controller/command', JointTrajectory, queue_size=10)
	rospy.init_node('move_head', anonymous=True)
	rate = rospy.Rate(10)

	head_pitch = 0.25
	head_yaw = 0.00
	incr_pitch = 0.10
	incr_yaw = 0.10
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
	msg = create_msg([0.25,0.00])
	pub.publish(msg)

# format data to trajectory_msgs format
def create_msg(positions):
	trajectory = JointTrajectory()
	point = JointTrajectoryPoint()
	trajectory.header.stamp = rospy.Time.now()
	trajectory.header.frame_id = "";

	trajectory.joint_names.append("HeadPitch");
	trajectory.joint_names.append("HeadYaw");

	for pose in positions:
		point.positions.append(pose)

	point.time_from_start.secs = 1
	point.time_from_start.nsecs = 0 

	trajectory.points.append(point)

	return trajectory

if __name__=='__main__':
    try:
        move_head()
    except rospy.ROSInterruptException:
        pass