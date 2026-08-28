import os
import subprocess
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, GroupAction, OpaqueFunction
from launch.conditions import IfCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription

def spawn_robots(context, *args, **kwargs):
    package_name = 'diff_drive_robot'
    package_dir = get_package_share_directory(package_name)
    world_path = os.path.join(package_dir, 'worlds', LaunchConfiguration('world').perform(context))
    urdf_xacro_path = os.path.join(package_dir, 'urdf', 'robot.xacro')
    bridge_config = os.path.join(package_dir, 'config', 'gz_bridge.yaml')

    actions = []

    # Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
        )]),
        launch_arguments={'gz_args': ['-r -v1 ', world_path], 'on_exit_shutdown': 'true'}.items()
    )
    actions.append(gazebo)

    # Генерируем URDF через xacro
    urdf_str = subprocess.check_output(['xacro', urdf_xacro_path], text=True)

    # Robot State Publisher
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': False,
            'robot_description': urdf_str,
        }],
    )
    actions.append(rsp_node)

    # Узел моста с этим файлом конфигурации
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p', 'expand_gz_topic_names:=true',
            '-p', f'config_file:={bridge_config}'
        ],
        output='screen'
    )
    actions.append(bridge_node)

    # Спавн робота через spawn (если работает)
    spawn_cmd = [
        'ros2', 'run', 'ros_gz_sim', 'create',
        '-topic', '/robot_description',
        '-name', 'diff_bot',
        '-x', '4.0',
        '-y', '0.0',
        '-z', '0.2'
    ]
    actions.append(ExecuteProcess(cmd=spawn_cmd, output='screen'))

    return actions

def generate_launch_description():
    package_name = 'diff_drive_robot'
    rviz = LaunchConfiguration('rviz')

    declare_world = DeclareLaunchArgument('world', default_value='office.world')
    declare_rviz = DeclareLaunchArgument('rviz', default_value='False')

    rviz_config = os.path.join(get_package_share_directory(package_name), 'rviz', 'bot.rviz')
    rviz2 = GroupAction(
        condition=IfCondition(rviz),
        actions=[Node(package='rviz2', executable='rviz2', arguments=['-d', rviz_config], output='screen')]
    )

    return LaunchDescription([
        declare_world,
        declare_rviz,
        rviz2,
        OpaqueFunction(function=spawn_robots)
    ])