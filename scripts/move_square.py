#!/usr/bin/env python3
import os
import rospy
from duckietown.dtros import DTROS, NodeType
from duckietown_msgs.msg import Twist2DStamped

class SquarePathNode(DTROS):
    def __init__(self, node_name):

        super(SquarePathNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        vehicle_name = os.environ['VEHICLE_NAME']
        twist_topic = f"/{vehicle_name}/car_cmd_switch_node/cmd"
        
        # Construct publisher
        self._publisher = rospy.Publisher(twist_topic, Twist2DStamped, queue_size=1)
        
    def run(self):
        rate = rospy.Rate(10)

        for _ in range(4):  # 4 sides of the square
            message = Twist2DStamped(v=0.3, omega=0.0)  # Forward movement
            for _ in range(34):  # Adjust based on how far you want to move (2 seconds at 10 Hz)
                self._publisher.publish(message)
                rate.sleep()

            message = Twist2DStamped(v=0.0, omega=4.5)  # 90-degree turn
            for _ in range(10):  # Adjust this based on how long it takes to turn 90 degrees
                self._publisher.publish(message)
                rate.sleep()
        
        # Stop after completing the square
        stop = Twist2DStamped(v=0.0, omega=0.0)
        self._publisher.publish(stop)
        
    def on_shutdown(self):
        # Stop the Duckiebot when shutting down
        stop = Twist2DStamped(v=0.0, omega=0.0)
        self._publisher.publish(stop)

if __name__ == '__main__':
    # Create the node
    node = SquarePathNode(node_name='square_path_node')
    # Run the node
    node.run()
    # Keep the process alive
    rospy.spin()
