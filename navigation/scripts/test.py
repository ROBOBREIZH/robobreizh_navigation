#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rosgraph.names import is_private
import rospy
from naoqi_bridge_msgs.msg import JointAnglesWithSpeed 

def dab():
    pub = rospy.Publisher('/joint_angles', JointAnglesWithSpeed, queue_size=10)
    rospy.init_node('make_it_dab', anonymous=True)
    rate = rospy.Rate(4)


    while not rospy.is_shutdown():
        msg = create_msg("LShoulder",["LShoulderRoll","LShoulderPitch"],[1.5,0.5])
        pub.publish(msg)
        msg = create_msg("LElbow",["LElbowRoll"],[0.0])
        pub.publish(msg)

        msg = create_msg("RShoulder",["RShoulderPitch"],[-0.4])
        pub.publish(msg)
        msg = create_msg("RElbow",["RElbowRoll","RElbowYaw"],[1.3,0.0])
        pub.publish(msg)

        msg = create_msg("Head",["HeadYaw","HeadPitch"],[-0.6,0.4])
        pub.publish(msg)

        msg = create_msg("Leg",["HipRoll"],[-0.5])
        pub.publish(msg)

        rate.sleep()

    msg = create_msg("Head",["HeadPitch","HeadYaw"],[0.15,0.00])
    pub.publish(msg) 


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
        dab()
    except rospy.ROSInterruptException:
        pass

