import os

<<<<<<< HEAD
from ament_index_python.packages import get_package_share_directory

=======

from ament_index_python.packages import get_package_share_directory
>>>>>>> e5fbb46 (fix depth camera orientation with camera_link_optical)

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch.actions import RegisterEventHandler, DeclareLaunchArgument
from launch.event_handlers import OnProcessStart, OnProcessExit

<<<<<<< HEAD
from launch_ros.actions import Node


import xacro


def generate_launch_description():

    rtabmap = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('rtabmap_launch'), 'launch', 'rtabmap.launch.py')]),
                launch_arguments={
                    'rtabmap_args': "--delete_db_on_start", 
                    'rgb_topic': "/omni_bot/front/image_raw",
                    'depth_topic': "/omni_bot/front/depth/image_raw",
                    'camera_info_topic': "/omni_bot/front/camera_info",
                    'frame_id': "base_link",
                    'approx_sync': "false",
                    'wait_imu_to_init': "false",
                    'imu_topic': "/omni_bot/imu",
                    'qos': "1",
                    'rviz': "false"
                    }.items()
            )
    # Launch!
    return LaunchDescription([
        rtabmap
=======
def generate_launch_description():
    return LaunchDescription([



         IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('rtabmap_launch'),'launch','rtabmap.launch.py'
                )]), launch_arguments={                
                    'rtabmap_args': "--delete_db_on_start" ,
                    'rgb_topic': "/diffbot/front/image_raw",
                    'depth_topic': "/diffbot/front/depth/image_raw",
                    'camera_info_topic': "/diffbot/front/camera_info",
                    'frame_id': "base_link",
                    'approx_sync': "false",
                    'wait_imu_to_init': "true",
                    'imu_topic': "/diffbot/imu",
                    'qos': "1",
                    'rviz': "true"
                }.items()

        )   

>>>>>>> e5fbb46 (fix depth camera orientation with camera_link_optical)
    ])
