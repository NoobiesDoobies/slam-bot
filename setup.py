from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'slam_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[

        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*.*')),
        (os.path.join('share', package_name, 'description'), glob('description/*.*')),
        (os.path.join('share', package_name, 'description/omni_urdf'), glob('description/omni_urdf/*.*')),
        (os.path.join('share', package_name, 'description/omni_urdf/STL'), glob('description/omni_urdf/STL/*.*')),
        (os.path.join('share', package_name, 'description/omni_urdf/wheel'), glob('description/omni_urdf/wheel/*.*')),
        (os.path.join('share', package_name, 'description/omni_urdf/base'), glob('description/omni_urdf/base/*.*')),
        (os.path.join('share', package_name, 'description/ros2_control'), glob('description/ros2_control/*.*')),
        (os.path.join('share', package_name, 'description/urdf'), glob('description/urdf/*.*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='carlios',
    maintainer_email='carlioseryan20@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'robot_localization = slam_bot.localization_node:main',
            "depth_to_laser_scan = slam_bot.depth_to_laser_scan_converter:main",
            'test = slam_bot.test:main',
            'velocity_remapper = slam_bot.velocity_remapper:main',
        ],
    },
)
