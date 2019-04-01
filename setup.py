#!/usr/bin/env python
import os
import re
from setuptools import setup, find_packages


def get_ini_variable(name):
    with open(os.path.join(os.path.dirname(__file__), 'src', 'ros_get', '__init__.py')) as f:
        return re.compile(r".*%s = '(.*?)'" % name, re.S).match(f.read()).group(1)


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as r_file:
    readme = r_file.read()

setup(
    name='ros_get',
    license='MIT',
    version=get_ini_variable('__version__'),
    url=get_ini_variable('__url__'),
    author=get_ini_variable('__author__'),
    author_email=get_ini_variable('__email__'),
    description='Simple tools for working with ROS source packages',
    long_description=readme,
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
        'rosdistro >= 0.7.3',
        'rosinstall_generator',
        'trollius',  # remove when catkin>0.4.4 is released
        'vcstools',
        'xdg==1.0.7',
    ],
    entry_points={'console_scripts': ['ros-get=ros_get.__main__:main']}, )
