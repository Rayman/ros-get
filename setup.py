#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='tue_tools',
    packages=find_packages('src'),  # include all packages under src
    package_dir={'': 'src'},  # tell distutils packages are under src
    install_requires=['rosdistro', 'vcstool'],
    scripts=['scripts/tue-get']
)
