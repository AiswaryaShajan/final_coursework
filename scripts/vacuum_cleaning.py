#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
twist = Twist()
pose = Pose()
print('Hey there! In order to clean your room, you have to tell me the coordinates of the four corners of your room, when prompted. See the example below: \n top-left corner : 3 <add a spac>e 4 if the corner is at (3,4)')

x1= 0
y1=0
x2= 11
y2=0
x3= 0
y3=11
x4=11
y4=11
reach_x2 = False
turned_90_on_left_once = False
moved_lil_straight= False
turned_90_on_left_twice = False
reached_x1 = False
turned_90_on_right_once =False
moved_lil_straight_again =False

def callback(msg):
    global pose, reached_x1
    pose=msg
def vacuum_cleaning():
    global pose, twist, get_time, x1,y1,x2,y2,x3,y3,x4,y4
    rospy.init_node('turtle_roomba', anonymous=True)
    pub = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/turtle2/pose', Pose, callback)
    rate = rospy.Rate(20)
    
    def move_horizontal():
        global reach_x2, turned_90_on_left_once, moved_lil_straight, turned_90_on_left_twice
        global reached_x1, moved_lil_straight_again
        if pose.x <x2:
            if reach_x2 == False:
                print('move right')
                twist.linear.x=2
                twist.angular.z=0
                pub.publish(twist)
                rospy.sleep(0.5)
        else:
            reach_x2=True
            twist.linear.x=0
            pub.publish(twist)
            if reach_x2 == True and turned_90_on_left_once == False:
                print('stopped to turn')
                twist.linear.x= 0
                twist.angular.z=1.5
                pub.publish(twist)
                turned_90_on_left_once = True
                rospy.sleep(0.5)
            elif turned_90_on_left_once and not moved_lil_straight:
                print('to move a lil straight')
                twist.angular.z=0
                twist.linear.x=2
                pub.publish(twist)
                rospy.sleep(0.5)
                moved_lil_straight = True
            elif moved_lil_straight and turned_90_on_left_twice== False:
                print("turning 90 again")
                twist.linear.x= 0
                twist.angular.z=4.7
                pub.publish(twist)
                turned_90_on_left_twice = True
                rospy.sleep(0.5)

            elif turned_90_on_left_twice and not reached_x1:
                while pose.x >x1 + 1: # just to make sure that it actually stops at the left end
                    twist.angular.z=0
                    print('lets move back')
                    twist.linear.x = 2
                    pub.publish(twist)
                    rospy.sleep(0.5)
                reached_x1 = True
                twist.linear.x = 0
                pub.publish(twist)
            elif reached_x1 and not turned_90_on_right_once:
                print('turn on right')
                twist.linear.x= 0
                twist.angular.z=1.5
                pub.publish(twist)
                turned_90_on_right_once = True
                rospy.sleep(0.5)
             





    while not rospy.is_shutdown():
        move_horizontal()
        rate.sleep()

        

if __name__=='__main__':
    try:
        vacuum_cleaning()
    except rospy.ROSInterruptException:
        pass