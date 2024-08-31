import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch.actions import RegisterEventHandler, DeclareLaunchArgument
from launch.event_handlers import OnProcessStart, OnProcessExit

from launch_ros.actions import Node



def generate_launch_description():
    
    package_name='slam_bot' 

    use_ros2_control = LaunchConfiguration('use_ros2_control')

    use_ros2_control_dec = DeclareLaunchArgument(
        'use_ros2_control',
        default_value='true',
        description='Use ros2 control if true'
    )

    tracker_params_sim = os.path.join(get_package_share_directory(package_name),'config','ball_tracker_params_sim.yaml')
    tracker_params_robot = os.path.join(get_package_share_directory(package_name),'config','ball_tracker_params_robot.yaml')


    robot_spawner = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','robot_spawner.launch.py'
                )]), launch_arguments={'sim_mode': 'true', 'use_ros2_control': use_ros2_control}.items()
    )

    joystick = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','joystick.launch.py'
                )])
    )


    # twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
    # twist_mux = Node(
    #         package="twist_mux",
    #         executable="twist_mux",
    #         parameters=[twist_mux_params],
    #         remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
    #     )

    


    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])

    controller_params_file = os.path.join(get_package_share_directory(package_name),'config','diffbot_controllers.yaml')


    gazebo_params_file = os.path.join(get_package_share_directory(package_name),'config','gazebo_params.yaml')

    world_file = os.path.join(
        get_package_share_directory("slam_bot"),
        # "worlds", "simple_wall_following.world"
        # "worlds", "maze_3_6x6.world"
        # "worlds", "self_made_maze.world"
        "worlds", "cafe.world"
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'world': world_file, 'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file }.items()
             )
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot',
                                   '-x', '0', '-y', '-1', '-z', '0.05',],
                        output='screen')

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diffbot_base_controller"],
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    rviz_config = os.path.join(get_package_share_directory(package_name),'rviz','rviz_config.rviz')

    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config]
    )


    # Launch them all!
    return LaunchDescription([
        use_ros2_control_dec,
        robot_spawner,
        gazebo,
        spawn_entity,
        # joystick,
        # twist_mux,
        # delayed_controller_manager,
        diff_drive_spawner,
        joint_broad_spawner,
        rviz2

    ])