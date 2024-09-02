import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped

class VelocityRemapper(Node):
    def __init__(self):
        super().__init__('velocity_remapper')
        self.publisher = self.create_publisher(TwistStamped, '/omni_wheel_controller/cmd_vel', 10)
        self.publisher2 = self.create_publisher(TwistStamped, '/diffbot_base_controller/cmd_vel', 10)

        self.subscription = self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        self.subscription

    def cmd_vel_callback(self, msg):
        # Remap the velocity here
        remapped_msg = Twist()
        remapped_msg.linear.x = -msg.linear.x
        remapped_msg.linear.y = msg.linear.y
        remapped_msg.angular.z = -msg.angular.z

        # Publish the remapped message in TwistStamped
        remapped_twist_stamped = TwistStamped()
        remapped_twist_stamped.header.stamp = self.get_clock().now().to_msg()
        remapped_twist_stamped.header.frame_id = 'base_frame_link'
        remapped_twist_stamped.twist = remapped_msg




        self.publisher.publish(remapped_twist_stamped)

def main(args=None):
    rclpy.init(args=args)
    velocity_remapper = VelocityRemapper()
    rclpy.spin(velocity_remapper)
    velocity_remapper.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()