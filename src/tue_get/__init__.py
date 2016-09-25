#!/usr/bin/env python
from __future__ import print_function

import logging
import os
from collections import OrderedDict
from collections import deque

from tue_get.utils import mkdir_p, update_folder, install_dependencies, get_rosdistro, get_rosdep

logger = logging.getLogger(__name__)


def get_workspace():
    workspace = os.getenv('TUE_WORKSPACE', None)
    return workspace


def get_distro():
    # TODO: get distro from environment
    distroname = 'tuekinetic'
    return distroname


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


def install(pkgs, verbose):
    workspace = get_workspace()
    target_path = os.path.join(workspace, 'src')
    distro = get_rosdistro(get_distro())

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

        updated_pkgs = update_folder(target_path, {repo: repository}, verbose)[repo]

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


def update(verbose):
    workspace = get_workspace()
    target_path = os.path.join(workspace, 'src')
    distro = get_rosdistro(get_distro())

    pkgs = get_pkgs_from_installed_list()

    # create a dict to remember which repos have been updated

    pkgs_queue = list(pkgs)
    pkgs_manifests = dict()
    repos_done = set()

    while pkgs_queue:
        # pop all packages from the queue
        packages = pkgs_queue
        pkgs_queue = list()

        # which repos are these packages in?
        repo_names = (distro.source_packages[package].repository_name for package in packages)

        # make unique
        repo_names = OrderedDict.fromkeys(repo_names).keys()

        # update the repos on disk
        folder_mapping = {repo: distro.repositories[repo] for repo in repo_names}
        updated_mapping = update_folder(target_path, folder_mapping, verbose)

        # potentially we updated more packages than we thought
        repos_done.update(repo_names)
        for repo, updated_packages in updated_mapping.items():
            for package in updated_packages:
                if verbose:
                    print('updated', package.name)

            pkgs_manifests.update({package.name: package for package in updated_packages})

        # get the dependencies of the packages we wanted to update
        deps = set()
        for package in packages:
            manifest = pkgs_manifests[package]

            # add deps of this package in the queue
            deps |= set(
                manifest.buildtool_depends +
                manifest.build_depends +
                manifest.run_depends +
                manifest.test_depends
            )

        # make deps unique
        deps = OrderedDict.fromkeys(dep.name for dep in deps).keys()

        for dep in deps:
            if dep not in distro.source_packages:
                # print('skipping', dep)
                continue
            repository_name = distro.source_packages[dep].repository_name
            if repository_name not in repos_done:
                logger.debug('queue: %s (%s)', dep, repository_name)
                pkgs_queue.append(dep)

    # install dependencies
    install_dependencies(target_path)


