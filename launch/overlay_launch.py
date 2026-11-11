import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = get_package_share_directory('overlaypkg')
    rviz_config_path = os.path.join(pkg_share, 'config', 'rvizconfig.rviz')
    return LaunchDescription([
        Node(
            package='overlaypkg',
            executable='overlay',
            name='overlay_node',
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config_path]
        )
    ])