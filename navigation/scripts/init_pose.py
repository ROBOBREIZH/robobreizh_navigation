#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rosgraph.names import is_private
import rospy
from naoqi_bridge_msgs.msg import JointAnglesWithSpeed 

def init_pose():
    pub = rospy.Publisher('/joint_angles', JointAnglesWithSpeed, queue_size=10)
    rospy.init_node('init_pos', anonymous=True)
    rate = rospy.Rate(4)

    while not rospy.is_shutdown():

        msg = create_msg("Head",["HeadYaw","HeadPitch"],[0.0,0.2])
        pub.publish(msg)

        msg = create_msg("Leg",["HipRoll"],[0.0])
        pub.publish(msg)

        rate.sleep()

def create_msg(frame_id,joint_names,joint_angles):
    trajectory = JointAnglesWithSpeed() 
    trajectory.header.stamp = rospy.Time.now()
    trajectory.header.frame_id = frame_id 

    trajectory.joint_names = joint_names
    trajectory.joint_angles = joint_angles

    trajectory.speed = 0.04
    trajectory.relative=0

    return trajectory

if __name__=='__main__':
    try:
        init_pose()
    except rospy.ROSInterruptException:
        pass

