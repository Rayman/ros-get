#!/usr/bin/env python
from __future__ import print_function

import errno
import logging
import os
from argparse import Namespace
from collections import OrderedDict
from collections import deque
from rosdep2 import RosdepLookup, create_default_installer_context, get_default_installer
from rosdep2.main import rosdep_main
from rosdep2.rospkg_loader import DEFAULT_VIEW_KEY

from catkin_pkg.packages import find_packages
from rosdistro import get_index, get_index_url, get_cached_distribution
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
    workspace = get_workspace()
    installed_dir = os.path.join(workspace, '.env', 'installed')

    mkdir_p(installed_dir)

    # touch the file
    for pkg in pkgs:
        logger.debug('marking for installation: %s', pkg)
        open(os.path.join(installed_dir, pkg), 'a').close()


def get_pkgs_from_installed_list():
    workspace = get_workspace()
    installed_dir = os.path.join(workspace, '.env', 'installed')

    return os.listdir(installed_dir)


def update_folder(target_path, folder_mapping):
    # generate rosinstall file
    config = generate_rosinstall_for_repos(folder_mapping, version_tag=False, tar=False)

    # convert it to the vcs format
    config = get_repos_in_rosinstall_format(config)

    # update the repos
    jobs = generate_jobs(config, Namespace(path=target_path))

    print('updating the following repositories:')
    output_repositories([job['client'] for job in jobs])

    print("let's start")
    results = execute_jobs(jobs, show_progress=True, number_of_workers=10)
    output_results(results)

    # which packages did we download?
    return {folder: find_packages(os.path.join(target_path, folder)).values() for folder in
            folder_mapping.keys()}


def get_rosdistro(distroname):
    index = get_index(get_index_url())
    distro = get_cached_distribution(index, distroname)
    return distro


def install_dependencies(path):
    args = ['install', '--from-paths', path, '--ignore-src', '--as-root', 'pip:false']
    rosdep_main(args)


def install(pkgs):
    distroname = get_distro()
    workspace = get_workspace()
    target_path = os.path.join(workspace, 'src')
    distro = get_rosdistro(distroname)

    add_pkgs_to_installed_list(pkgs)

    # TODO: check if the packages extist

    # which repo should this package be in?
    repo_names = (distro.source_packages[pkg].repository_name for pkg in pkgs)
    # make unique
    repo_names = OrderedDict.fromkeys(repo_names).keys()
    repos_queue = deque(repo_names)
    repos_done = set()

    while repos_queue:
        print('%d more repositories in the queue:' % len(repos_queue), repos_queue)

        repo = repos_queue.popleft()
        repos_done.add(repo)
        repository = distro.repositories[repo]

        updated_pkgs = update_folder(target_path, {repo: repository})[repo]

        deps = set()
        for name, updated_pkg in updated_pkgs.items():
            print('updated:', name)

            # add deps of this package in the queue
            deps |= set(
                updated_pkg.buildtool_depends +
                updated_pkg.build_depends +
                updated_pkg.run_depends +
                updated_pkg.test_depends
            )

        # make deps unique
        deps = OrderedDict.fromkeys(dep.name for dep in deps).keys()

        for dep in deps:
            if dep not in distro.source_packages:
                print('skipping', dep)
                continue
            repository_name = distro.source_packages[dep].repository_name
            if repository_name not in repos_queue and repository_name not in repos_done:
                print('queue:', repository_name)
                repos_queue.append(repository_name)

    # install dependencies
    install_dependencies(target_path)


def update():
    distroname = get_distro()
    workspace = get_workspace()
    target_path = os.path.join(workspace, 'src')
    distro = get_rosdistro(distroname)

    pkgs = get_pkgs_from_installed_list()
    repos = os.listdir(target_path)

    # create a dict to remember which repos have been updated
    repos = dict.fromkeys(repos)

    pkgs_queue = deque(pkgs)
    pkgs_done = set()

    while pkgs_queue:
        # which repos are these packages in?
        repo_names = (distro.source_packages[pkg].repository_name for pkg in pkgs)

        # make unique
        repo_names = OrderedDict.fromkeys(repo_names).keys()

        # get all corresponding repositories
        repositories = (distro.repositories[repo] for repo in repo_names)

        print(list(repositories))
        return

        # updated_pkgs = update_folder(target_path, {repo: repository})[repo]        return


def get_workspace():
    workspace = os.getenv('TUE_WORKSPACE', None)
    return workspace


def get_distro():
    # TODO: get distro from environment
    distroname = 'tuekinetic'
    return distroname


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
