from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=[
                'xterm', '-e', 
                'ros2', 'run', 'teleop_twist_keyboard', 'teleop_twist_keyboard', 
                '--ros-args', '--remap', 'cmd_vel:=/diffbot_base_controller/cmd_vel', '-p', 'stamped:=true'
            ],
            output='screen'
        )
    ])