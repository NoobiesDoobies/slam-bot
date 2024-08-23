import rclpy
from rclpy.node import Node

class LocalizationNode(Node):
    def __init__(self):
        super().__init__('localization_node')
        self.get_logger().info('Localization node initialized')

def main(args=None):
    rclpy.init(args=args)
    node = LocalizationNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()