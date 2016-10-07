#!/usr/bin/env python
from __future__ import print_function

import errno
import logging
import os
from collections import OrderedDict

from ros_get.utils import mkdir_p, update_folder, install_dependencies, get_rosdistro, get_rosdep

logger = logging.getLogger(__name__)


def add_pkgs_to_installed_list(pkgs):
    from . import installed_dir
    mkdir_p(installed_dir)

    # touch the file
    for pkg in pkgs:
        logger.debug('marking for installation: %s', pkg)
        open(os.path.join(installed_dir, pkg), 'a').close()


def get_pkgs_from_installed_list():
    from . import installed_dir
    return os.listdir(installed_dir)


def remove_pkgs_from_installed_list(pkgs):
    from . import installed_dir
    for pkg in pkgs:
        try:
            os.remove(os.path.join(installed_dir, pkg))
        except OSError as e:
            if e.errno == errno.ENOENT:
                print('E: Unable to locate package', pkg)
            else:
                raise
        else:
            print('Removing', pkg)


def install(pkgs, verbose):
    from . import target_path
    add_pkgs_to_installed_list(pkgs)

    pkgs_queue = list(pkgs)
    repos_done = set(os.listdir(target_path))

    recursive_update(pkgs_queue, repos_done, verbose)


def update(verbose):
    pkgs = get_pkgs_from_installed_list()

    pkgs_queue = list(pkgs)
    repos_done = set()

    recursive_update(pkgs_queue, repos_done, verbose)


def remove(pkgs, verbose):
    remove_pkgs_from_installed_list(pkgs)


def recursive_update(pkgs_queue, repos_done, verbose):
    from . import target_path, link_dir

    # TODO: get distro from environment
    distro = get_rosdistro('tuekinetic')

    # create a dict to remember which repos have been updated
    pkgs_manifests = dict()

    # remember visited packages, to symlink later
    pkgs_done = list()

    while pkgs_queue:
        # pop all packages from the queue
        packages = pkgs_queue
        pkgs_queue = list()

        # check for unknown packages
        unknown_packages = [package for package in packages if package not in distro.source_packages]
        packages = [package for package in packages if package in distro.source_packages]
        if unknown_packages:
            logger.error('Unknown packages: %s', ','.join(unknown_packages))

        # which repos are these packages in?
        repo_names = (distro.source_packages[package].repository_name for package in packages)

        # make unique
        repo_names = OrderedDict.fromkeys(repo_names).keys()

        # update the repos on disk
        folder_mapping = {repo: distro.repositories[repo] for repo in repo_names}
        updated_mapping = update_folder(target_path, folder_mapping, verbose)
        # import ipdb; ipdb.set_trace()

        # potentially we updated more packages than we thought
        repos_done.update(repo_names)
        for repo, updated_packages in updated_mapping.items():
            for folder, package in updated_packages.items():
                path = os.path.join(repo, folder)
                if verbose:
                    print('updated', package.name, '(', path, ')')
            pkgs_manifests.update({package: os.path.join(repo, folder) for folder, package in updated_packages.items()})

        # get the dependencies of the packages we wanted to update
        deps = set()
        for package in packages:
            manifest = next(manifest for manifest in pkgs_manifests if manifest.name == package)
            # manifest = pkgs_manifests[package]

            # add deps of this package in the queue
            deps |= set(
                manifest.buildtool_depends +
                manifest.build_depends +
                manifest.run_depends +
                manifest.test_depends
            )

        pkgs_done.extend(packages)

        # make deps unique
        deps = OrderedDict.fromkeys(dep.name for dep in deps).keys()

        for dep in deps:
            if dep not in distro.source_packages:
                if get_rosdep(dep):
                    logger.debug('skipping rosdep: %s', dep)
                else:
                    logger.warn('unknown dependency: %s', dep)
                continue
            repository_name = distro.source_packages[dep].repository_name
            if repository_name not in repos_done:
                logger.debug('queue: %s (%s)', dep, repository_name)
                pkgs_queue.append(dep)

    mkdir_p(link_dir)
    for package in pkgs_done:
        manifest = next(manifest for manifest in pkgs_manifests if manifest.name == package)
        folder = pkgs_manifests[manifest]

        print('linking', package, '==>', folder)

        source = os.path.join(target_path, folder)
        link_name = os.path.join(link_dir, package)

        try:
            os.symlink(source, link_name)
        except OSError as e:
            if e.errno == errno.EEXIST:
                if os.readlink(link_name) == source:
                    print('\tOK')
                else:
                    print('\tE: File exists')
            else:
                raise

    # install dependencies
    install_dependencies(target_path)


def upgrade(verbose):
    pass
