import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry

class LocalizationNode(Node):
    def __init__(self):
        super().__init__('localization_node')
        self.get_logger().info('Localization node initialized')
        
        # Object attributes
        self.imu_data = None
        self.ground_truth_data = None
        self.odom_data = None

        # Subscribers
        self.imu_subscriber = self.create_subscription(
            Imu,
            '/diffbot/imu',
            self.imu_callback,
            10
        )

        self.ground_truth_subscriber = self.create_subscription(
            Odometry,
            '/p3d/ground_truth',
            self.ground_truth_callback,
            10
        )

        self.odom_subscriber = self.create_subscription(
            Odometry,
            '/diffbot_base_controller/odom',
            self.odom_callback,
            10
        )

    def imu_callback(self, msg):
        self.get_logger().info('Received IMU data') 
        self.imu_data = msg

    def ground_truth_callback(self, msg):
        self.get_logger().info('Received ground truth data')
        self.ground_truth_data = msg

    def odom_callback(self, msg):
        self.get_logger().info('Received odometry data')
        self.odom_data = msg

def main(args=None):
    rclpy.init(args=args)
    node = LocalizationNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()