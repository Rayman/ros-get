#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='ros_get',
    package_dir={'': 'src'},  # tell distutils packages are under src
    packages=find_packages('src'),  # include all packages under src
    install_requires=['xdg', 'rosdistro', 'vcstool', 'colorlog', 'rosinstall_generator'],
    entry_points={
        'console_scripts': [
            'ros-get=ros_get.__main__:main'
        ]
    },
)
