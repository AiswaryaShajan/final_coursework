#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
twist = Twist()
pose = Pose()
print('Hey there! In order to clean your room, you have to tell me the coordinates of the four corners of your room, when prompted. See the example below: \n top-left corner : 3 <add a spac>e 4 if the corner is at (3,4)')
x1, y1 = map(float, input("Bottom left corner : ").split())
x2, y2 = map(float, input("Bottom right corner: ").split())
x3, y3 = map(float, input("Top left corner : ").split())
x4, y4 = map(float, input("Top right corner: ").split())
get_time = None

def callback(msg):
    rospy.loginfo(f"The Turtle is at x= {msg.x}, y= {msg.y}")
    global pose
    pose=msg

def vacuum_cleaning():
    global pose, twist, get_time, x1,y1,x2,y2,x3,y3,x4,y4
    rospy.init_node('turtle_roomba', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    rate = rospy.Rate(10)
    time = (x2-x1)/2
    
    while not rospy.is_shutdown() and pose.x < x2:
        twist.linear.x=2
        pub.publish(twist)        
        rate.sleep()
        

if __name__=='__main__':
    try:
        vacuum_cleaning()
    except rospy.ROSInterruptException:
        pass