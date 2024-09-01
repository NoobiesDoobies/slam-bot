import os
import math

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, FindExecutable, Command

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

import xacro

ROBOT1_START_POSITION    = [0.0, 0.0, 0.0]
ROBOT1_START_YAW = 0.0
def generate_launch_description():
    # Launch Arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)
    package_name = 'slam_bot'


    gazebo_params_file = os.path.join(get_package_share_directory(package_name),'config','gazebo_params.yaml')

    world_file = os.path.join(
        get_package_share_directory("slam_bot"),
        "worlds", "furnished_office.world"
    )
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'world': world_file, 'verbose': 'false', 'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file }.items()
             )
    # gazebo = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    # )

    xacro_file = os.path.join(package_name,
                              'description', 'omni_urdf',
                              'robot.urdf.xacro')
    robot_description_config = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("slam_bot"), "description", "omni_urdf", "robot.urdf.xacro"]
            ),
            " ",

        ]
    )
    params = {'robot_description': robot_description_config}

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters  =[params],
        remappings=[
            ('/omni_wheel_controller/cmd_vel', '/cmd_vel'),
        ],
    )

    gz_spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        output='screen',
        arguments=['-topic', 'robot_description',
                   '-entity', 'omnibot',
                   '-x', str(ROBOT1_START_POSITION[0]),
                   '-y', str(ROBOT1_START_POSITION[1]),
                   '-z', str(ROBOT1_START_POSITION[2]),
                   '-R', str(0.0),
                   '-P', str(0.0),
                   '-Y', str(ROBOT1_START_YAW),
                   ],
    )

    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_omni_wheel_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'omni_wheel_controller'],
        output='screen'
    )


    omni_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["omni_wheel_controller"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )
    
    # Bridge
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[ 
                   '/camera_info@sensor_msgs/msg/CameraInfo@ignition.msgs.CameraInfo',
                   '/image_raw@sensor_msgs/msg/Image@ignition.msgs.Image',
                  ],
        output='screen'
    )

    # velocity_converter = Node(
    #     package='velocity_pub',
    #     name='velocity_pub',
    #     executable='velocity_pub',
    #     remappings=[
    #         ('/cmd_vel_stamped', '/omni_wheel_controller/cmd_vel'),
    #     ],
    # )

    
    rviz_config_file = os.path.join(get_package_share_directory(package_name),'rviz','omni_rviz_config.rviz')
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )
    
    return LaunchDescription([
        # RegisterEventHandler(
        #     event_handler=OnProcessExit(
        #         target_action=gz_spawn_entity,
        #         on_exit=[load_joint_state_controller],
        #     )
        # ),
        # RegisterEventHandler(
        #     event_handler=OnProcessExit(
        #        target_action=load_joint_state_controller,
        #        on_exit=[load_omni_wheel_controller],
        #     )
        # ),
        gazebo,
        omni_drive_spawner,
        joint_broad_spawner,
        node_robot_state_publisher,
        gz_spawn_entity,
        bridge,
        # velocity_converter,
        # rviz,
    ]
    )