from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node
from rclpy.time import Time
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy
from sensor_msgs.msg import Image

class ImageListenerNode(Node):
    def __init__(self) -> None:
        super().__init__("image_node")
        self.cb_group = ReentrantCallbackGroup()

        self.declare_parameter("view_rate", 10)
        self.declare_parameter("color_topic", "rgbd_camera/image")
        self.declare_parameter("depth_topic", "rgbd_camera/depth_image")

        self.view_rate = int(self.get_parameter("view_rate").value)
        self.color_topic = str(self.get_parameter("color_topic").value)
        self.depth_topic = str(self.get_parameter("depth_topic").value)

        self.color_sub = self.create_subscription(
            Image,
            self.color_topic,
            self._color_cb,
            10,
            callback_group=self.cb_group
        )

        self.depth_sub = self.create_subscription(
            Image,
            self.depth_topic,
            self._depth_cb,
            10,
            callback_group=self.cb_group
        )

        self.get_logger().info(
            f"Listening RGBD Camera on {self.color_topic} and {self.depth_topic}."
        )

    # ------------------------ ROS callbacks ------------------------

    def _color_cb(self, msg: Image) -> None:
        self.get_logger().info(
            f"Received color image: {msg.width}x{msg.height}, "
            f"data={msg.data}"
        )

    def _depth_cb(self, msg: Image) -> None:
        self.get_logger().info(
            f"Received depth image: {msg.width}x{msg.height}, "
            f"data={msg.data}"
        )


