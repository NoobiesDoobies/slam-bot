import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, OpaqueFunction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def include_joystick(context, *args, **kwargs):
    is_joystick = LaunchConfiguration('isJoystick').perform(context)
    if is_joystick.lower() == 'true':
        package_name = 'slam_bot'
        return [IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory(package_name), 'launch', 'joystick.launch.py'
            )]), launch_arguments={'use_sim_time': 'true'}.items()
        )]
    return []

def generate_launch_description():
    # Declare the launch argument
    is_joystick_arg = DeclareLaunchArgument(
        'isJoystick',
        default_value='False',
        description='Flag to enable joystick launch'
    )

    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    package_name = 'slam_bot'  # <--- CHANGE ME

    robot_spawner = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'robot_spawner.launch.py'
        )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    gazebo_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'gazebo_params.yaml')

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()
    )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )

    # Launch them all!
    return LaunchDescription([
        is_joystick_arg,
        robot_spawner,
        OpaqueFunction(function=include_joystick),
        gazebo,
        spawn_entity,
        diff_drive_spawner,
        joint_broad_spawner
    ])