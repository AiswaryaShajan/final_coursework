#!/usr/bin/env python3 
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from pynput.keyboard import Key, Listener
twist = Twist() # Declaring the global variables so that they can be accessed in any of the functions.
pose= Pose()
last_pressed_key = None

def wall_avoidance():
    rospy.init_node('wall_avoidance', anonymous=True)
    rate=rospy.Rate(10)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    def callback(data): # data is a local variable. it can only be used inside the callback function.
        global pose
        pose=data   #it has to be stored somewhere so that it can be accessed outside the callback.
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    print('Use keys to move:\n"w" for forward\n"s" for reverse\n"a" for rotate left\n"d" for rotate right.')
    def on_press(key):
        global twist, pose, last_pressed_key
        try:
            if key.char in ['w','a','s','d']:
                if 1.6 < pose.x < 9.4 and 1.6<pose.y<9.4: #Boundary condition
                    print('Turtle is within bounds!')
                    twist.angular.z = 0 # to reset angular velocity, else even if it was in the boundary, it would circle continously.
                    if key.char == 'w':
                        twist.linear.x = 2
                        last_pressed_key = 'w'
                    elif key.char == 'a':
                        twist.angular.z= 2
                    elif key.char == 's':
                        twist.linear.x = -2
                        last_pressed_key = 's'
                    elif key.char == 'd':
                        twist.angular.z= -2
                elif last_pressed_key in ['w','s']:
                    twist.angular.z = 3
                    pub.publish(twist)
                    rospy.Duration(0.5) # precaution to ensure messages dont get overlapped and turtle doesnt skip boundary.
                    if last_pressed_key == 'w':
                        print('Oops!..you are off-limits! press "w" to get back in')
                        if key.char == 'w':
                            twist.linear.x=2
                        if key.char == 's':
                            twist.linear.x =0
                            twist.angular.z=0
                    if last_pressed_key == 's':
                        print('Oops! ..you are off-limits! press "s" to get back in')
                        if key.char == 's':
                            twist.linear.x= -2
                        if key.char == 'w':
                            twist.linear.x=0
                            twist.angular.z=0
                    if key.char in ['a','d']: #Disabling rotation at boundary
                        twist.linear.x = 0
                        twist.angular.z =0
            pub.publish(twist)
        except AttributeError:
            pass
    def on_release(key):
        global twist
        global pose
        try:
            if key.char in ['w', 'a', 's', 'd']:
                twist.linear.x = 0
                twist.angular.z = 0
                pub.publish(twist)
        except AttributeError:
            pass    
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
        
    
    while not rospy.is_shutdown():
        rate.sleep()
    else:
        listener.stop()

if __name__== "__main__":
    try:
        wall_avoidance()
    except rospy.ROSInterruptException:
        pass