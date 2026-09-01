from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node
from rclpy.time import Time
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from geometry_msgs.msg import Twist

class MotionControlNode(Node):
    def __init__(self) -> None:
        super().__init__("image_node")
        self.cb_group = ReentrantCallbackGroup()

        self.declare_parameter("motion_topic", "/cmd_vel")

        self.motion_topic = str(self.get_parameter("motion_topic").value)

        self.motion_pub = self.create_publisher(
            Twist,
            self.motion_pub,
            10,
            callback_group=self.cb_group
        )

        self.get_logger().info(
            f"Publishing motion to {self.motion_topic}."
        )

    def move_robot(self, input_twist: Twist):
        self.get_logger.info(
            f"Publishing {input_twist} to {self.motion_topic}."
        )
        self.motion_pub.publish(input_twist)
