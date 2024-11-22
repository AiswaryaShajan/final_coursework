#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from pynput.keyboard import Key, Listener, KeyCode


speed = 1                                                                                  # initialising the value outside the function makes it a global variable that can be modified later.
def teleoperation():                                                                       #Teleoperation function to be called in the "main"
    rospy.init_node('teleop', anonymous=True)
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)                        #Created node that publishes to the cmd_vel topic
    rate = rospy.Rate(10)
    twist = Twist()

    def on_press(key):                                                                     #Function defined for when pressing up, down, left and right arrow keys
        global speed                                                                       #global keyword is to be used when accessing the variable from outside. This helps in changing the speed across the entire code.
        try:
            if key == Key.up:
                twist.linear.x = speed
            elif key == Key.down:
                twist.linear.x = -speed
            elif key == Key.left:
                twist.angular.z = speed
            elif key == Key.right:
                twist.angular.z = -speed
            elif key == Key.esc:                                                           # Esc key added to quit the node.
                print('\n\nTeleoperation terminated.')
                rospy.signal_shutdown("Escape key pressed")                                # shuts down the ROS Node first before the listener for a clean exit. Here  a reason is passed as argument so that its executed.
                return False                                                                # shuts down the listener
            elif key == KeyCode.from_char('+'):
                speed += 0.1                                                                #increase speed
                print(f"Speed increased to: {speed}")
            elif key == KeyCode.from_char('-'):                                                           #reduce speed
                speed -= 0.1
                print(f"Speed decreased to: {speed}")
            else:
                pass
        except AttributeError:                                                             #To handle special keys, that may not have a similar attrbute.
            pass

    def on_release(key):                                                                    #Function defined for when releasing arrow keys
        try:
            if key == Key.up:
                twist.linear.x = 0
            elif key == Key.down:
                twist.linear.x = 0
            elif key == Key.left:
                twist.angular.z = 0
            elif key == Key.right:
                twist.angular.z = 0
        except AttributeError:  
            pass
    try:
        listener = Listener(on_press=on_press, on_release=on_release)                          #Listener called after defining the press/release func. 
        listener.start()
    except KeyboardInterrupt:  
        pass                                                                     #Non-blocking way that itself is a loop that runs on its own in the background. No need to loop it.
    print('Press the arrow keys to move','\n---------------------------','\nPress "+" key to increase speed and "-" key to decrease the speed','\nPress "esc" key to quit.')           
    while not rospy.is_shutdown():                                                         # To run the node in a loop, so that it publishes continously.
        pub.publish(twist)
        rate.sleep()
    
    listener.stop()                                                                       #Listener in pynput runs its own thread. To ensure that the listener is properly stopped after the node shuts down (ctrl C)
if __name__ == '__main__':
    try:
        teleoperation()
    except rospy.ROSInterruptException:                                                   # Handles ctrl c gracefully.
        pass



        
        



