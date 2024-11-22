#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
rospy.init_node('turtle_roomba', anonymous=True)
pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
pose = Pose()
twist=Twist()
def pose_callback(data):
    global pose
    pose = data

rospy.Subscriber('/turtle2/pose', Pose, pose_callback)