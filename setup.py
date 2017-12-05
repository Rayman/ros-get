#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='ros_get',
    package_dir={'': 'src'},  # tell distutils packages are under src
    packages=find_packages('src'),  # include all packages under src
    install_requires=[
        'argcomplete',
        'catkin_pkg',
        'catkin_tools',
        'colorlog',
        'future',
        'mock',
        'rosdep',
        'rosdistro',
        'rosinstall_generator',
        'trollius',  # remove when catkin>0.4.4 is released
        'vcstool',
        'xdg==1.0.7',
    ],
    entry_points={'console_scripts': ['ros-get=ros_get.__main__:main']}, )
