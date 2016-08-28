#!/usr/bin/env python

from rosinstall_generator.distro import get_recursive_dependencies
from rosdistro import get_cached_distribution, get_index, get_index_url
from rosdistro.dependency_walker import DependencyWalker, SourceDependencyWalker


distro = 'tuekinetic'
index = get_index(get_index_url())
distro = get_cached_distribution(index, distro)

walker = SourceDependencyWalker(distro)
dependencies = walker.get_recursive_depends('navigation', ['buildtool', 'build', 'run', 'test'],
                                            ros_packages_only=True, ignore_pkgs=None, limit_depth=None)

for dep in dependencies:
    print dep

