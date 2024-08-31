import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ekf_config = os.path.join(
        get_package_share_directory('slam_bot'),
        'config',
        'ekf_config.yaml'
    )

    return LaunchDescription([
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[ekf_config],
            remappings=[
                ('/odometry/filtered', '/odometry/filtered')
            ]
        ),
        # Node(
        #     package='slam_bot',
        #     executable='robot_localization',
        #     name='robot_localization',
        #     output='screen'
        # )
    ])