#!/usr/bin/env python
from __future__ import print_function

import errno
import logging
import os
from argparse import Namespace
from rosdep2 import RosdepLookup, create_default_installer_context, get_default_installer
from rosdep2.main import rosdep_main
from rosdep2.rospkg_loader import DEFAULT_VIEW_KEY

from rosdistro import get_index, get_index_url, get_cached_distribution
from rosdistro.dependency_walker import SourceDependencyWalker
from rosinstall_generator.generator import generate_rosinstall_for_repos
from vcstool.commands.import_ import (generate_jobs, get_repos_in_rosinstall_format, output_repositories, execute_jobs,
                                      output_results)

logger = logging.getLogger(__name__)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def add_pkgs_to_installed_list(pkgs):
    workspace = os.getenv('TUE_WORKSPACE', None)
    installed_dir = os.path.join(workspace, '.env', 'installed')

    mkdir_p(installed_dir)

    # touch the file
    for pkg in pkgs:
        logger.debug('marking for installation: %s', pkg)
        open(os.path.join(installed_dir, pkg), 'a').close()


def install_dependencies(path):
    args = ['install', '--from-paths', path, '--ignore-src', '--as-root', 'pip:false']
    rosdep_main(args)


def install(pkgs):
    # TODO: get distro from environment
    distroname = 'tuekinetic'
    workspace = os.getenv('TUE_WORKSPACE', None)
    target_path = os.path.join(workspace, 'src')

    # TODO: check if the packages extist

    add_pkgs_to_installed_list(pkgs)

    # let's figure out the dependent packages

    index = get_index(get_index_url())
    distro = get_cached_distribution(index, distroname)

    # which repo should this package be in?
    package = pkgs[0]
    repository_name = distro.source_packages[package].repository_name
    repository = distro.repositories[repository_name]


    print(pkgs, repository.name)

    return

    print('The following packages will be installed:')
    for package in packages:
        print(' ', package)

    # now let's figure out which repos these dependencies belong
    repos = {}
    for package in packages:
        repository_name = distro.source_packages[package].repository_name
        repository = distro.repositories[repository_name]

        # TODO: check duplicates
        repos[repository_name] = repository

    # generate a rosinstall file
    config = generate_rosinstall_for_repos(repos, version_tag=False, tar=False)

    # convert it to the vcs format
    config = get_repos_in_rosinstall_format(config)

    jobs = generate_jobs(config, Namespace(path=target_path))
    print('updating the following repositories:')
    output_repositories([job['client'] for job in jobs])

    results = execute_jobs(jobs, show_progress=True, number_of_workers=10)
    output_results(results)

    # install dependencies
    install_dependencies(target_path)


cached_view = None


def get_rosdep(key):
    installer_context = create_default_installer_context(verbose=False)

    installer, installer_keys, default_key, \
    os_name, os_version = get_default_installer(installer_context=installer_context,
                                                verbose=False)

    global cached_view
    if not cached_view:
        lookup = RosdepLookup.create_from_rospkg()
        lookup.verbose = False

        view = lookup.get_rosdep_view(DEFAULT_VIEW_KEY, verbose=False)
        cached_view = view
    else:
        view = cached_view

    try:
        d = view.lookup(key)
        rule_installer, rule = d.get_rule_for_platform(os_name, os_version, installer_keys, default_key)
        return rule_installer, rule
    except KeyError as e:
        return False
