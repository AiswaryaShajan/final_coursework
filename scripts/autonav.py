#!/usr/bin/env python3
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
from turtlesim.srv import SetPen  # Import the SetPen service

# Initialize the ROS node
rospy.init_node('navigation_node', anonymous=True)

# Publisher for turtle velocity
pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

# Taking user input for target coordinates
a, b = map(float, input('Enter the coordinates separated by a space. Make sure the values are between 0 and 11: ').split())
print(f"Lets go to: ({a}, {b})")

# Initialize twist message
twist = Twist()
twist.linear.x = 0
twist.angular.z = 0

# Flags to track rotation and linear movement
rotation_done = False
linear_done = False

# Lift the pen before starting any movement
def lift_pen():
    try:
        # Wait for the set_pen service to become available
        rospy.wait_for_service('/turtle1/set_pen', timeout=5)
        set_pen = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
        set_pen(0, 0, 0, 0, 1)  # (r=0, g=0, b=0, width=0, off=1 to completely turn off drawing)
        print("Pen lifted and drawing disabled.")
    except rospy.ROSException as e:
        print("Failed to lift pen: %s" % e)

# Callback function for pose
def callback(pose):
    global rotation_done
    global linear_done
    rate = rospy.Rate(10)
    
    # Calculate the target angle and distance
    y = b - pose.y
    x = a - pose.x
    angle_to_target = math.atan2(y, x)
    distance_to_target = math.sqrt((a - pose.x)**2 + (b - pose.y)**2)
    angle_difference = abs(angle_to_target - pose.theta)

    # Check if we need to rotate
    if not rotation_done:
        if angle_difference > 0.04:
            twist.angular.z = 2
            pub.publish(twist)
        else:
            twist.angular.z = 0
            pub.publish(twist)
            rotation_done = True
            rate.sleep()
    else:
        # Move forward if rotation is done
        if not linear_done:
            if distance_to_target > 0.3:
                twist.linear.x = 1
                pub.publish(twist)
            else:
                linear_done = True
        else:
            # Stop moving when the destination is reached
            twist.linear.x = 0
            pub.publish(twist)
            print("Destination arrived. Aloha!")
            print(f"\nwe are actually at x= {pose.x}, y= {pose.y}...it's still a work in progress...")

            
            rospy.signal_shutdown('destination reached')

# Subscriber function
def subscriber():
    rospy.Subscriber('/turtle1/pose', Pose, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        lift_pen()  # Lift the pen right at the beginning before movement
        subscriber()
    except rospy.ROSInterruptException:
        pass
