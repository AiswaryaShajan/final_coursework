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
    pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle2/pose', Pose, callback)
    rate = rospy.Rate(10)
    time = (x2-x1)/2
    
    def move_horizontal():
        if pose.x < x2:
            print('move right')
            twist.linear.x=2
            twist.angular.z=0
            pub.publish(twist)
            rospy.sleep(0.5)
        else:
            print('turning now')
            twist.linear.x= 0
            twist.angular.z=1.5
            pub.publish(twist)
            rospy.sleep(0.5)
            print('going straight for a while')
            twist.linear.x= 2
            twist.angular.z=0
            pub.publish(twist)
            rospy.sleep(0.5)
            print('turning again')
            twist.linear.x= 0
            twist.angular.z=1.5
            pub.publish(twist)
            rospy.sleep(0.5)
            if pose.x >= x1:
                print('move left')
                twist.linear.x= 2
                twist.angular.z=0
                
            else:
                print('reached and turning back')
                twist.linear.x=0
                twist.angular.z = 3
            pub.publish(twist)


    while not rospy.is_shutdown():
        move_horizontal()
        rate.sleep()

        

if __name__=='__main__':
    try:
        vacuum_cleaning()
    except rospy.ROSInterruptException:
        pass