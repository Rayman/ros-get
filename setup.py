#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='ros_get',
    packages=find_packages('src'),  # include all packages under src
    package_dir={'': 'src'},  # tell distutils packages are under src
    install_requires=['rosdistro', 'vcstool', 'colorlog', 'rosinstall_generator'],
    scripts=['scripts/ros-get', 'scripts/ros-status', 'scripts/ros-env']
)
