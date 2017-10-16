#!/usr/bin/env python
from __future__ import print_function

import logging
import os
from Queue import Queue, Empty
from collections import OrderedDict

from .utils import mkdir_p, get_rosdistro, update_folder
from .workspace import ws_file

logger = logging.getLogger(__name__)
installed_dir = os.path.join(ws_file, '.env', 'installed')
target_path = os.path.realpath(os.path.join(ws_file, 'repos'))


def install(pkgs, verbose):
    mkdir_p(target_path)

    # TODO: get distro from environment
    distro = get_rosdistro('tuekinetic')

    pkgs_queue = Queue()
    for pkg in pkgs:
        pkgs_queue.put_nowait(pkg)

    repos_done = set()

    # mapping from manifest to found location
    pkgs_manifests = {}

    try:
        while True:
            pkg = pkgs_queue.get_nowait()

            if len([m for m in pkgs_manifests if m.name == pkg]):
                continue

            repo = [repo for repo in distro.repositories.values() if pkg in repo.source_repository.patched_packages]
            if len(repo) == 0:
                logger.debug("Package '%s' can't be found in a repository", pkg)
                continue

            logger.info('installing: %s', pkg)

            assert len(repo) == 1, "Package '%s' is in multiple repositories" % pkg
            repo = repo[0]

            # TODO: check if repo was already updated

            updated_mapping = update_folder(target_path, {repo.name: repo}, verbose)

            for folder, updated_packages in updated_mapping.items():

                # first check for expected packages that were not found
                found_names = set(package.name for package in updated_packages.values())
                for package in repo.source_repository.patched_packages:
                    if package not in found_names:
                        logger.warning("Package '%s' not found in the repo: '%s'", package, repo.name)

                # then check for found packages that were not in the yaml
                for subfolder, package in updated_packages.items():
                    if package.name in repo.source_repository.patched_packages:
                        print('adding %s' % os.path.join(folder, subfolder))
                        pkgs_manifests[package] = os.path.join(folder, subfolder)
                    else:
                        logger.debug("Found package '%s' in an unexpected repo: '%s'", package.name, repo.name)

            manifest = [m for m in pkgs_manifests if m.name == pkg]
            if not len(manifest):
                logger.error("Required package '%s' not found", pkg)
                return 1
            assert len(manifest) == 1
            manifest = manifest[0]

            repos_done.add(repo)

            deps = manifest.buildtool_depends + manifest.build_depends + manifest.run_depends + manifest.test_depends
            for dep in deps:
                # try to get the manifest of the dep
                if not len([m for m in pkgs_manifests if m.name == dep.name]):
                    logger.debug("queing: '%s'", dep.name)
                    pkgs_queue.put_nowait(dep.name)

    except Empty:
        pass
    if not repos_done:
        logger.error('no repository updated, package could not be found')
        return 1

    print('OK')


def update(verbose):
    pass


def remove(pkgs, verbose):
    pass


def upgrade(verbose):
    pass


def add_pkgs_to_installed_list(pkgs):
    mkdir_p(installed_dir)

    # touch the file
    for pkg in pkgs:
        logger.debug('marking for installation: %s', pkg)
        open(os.path.join(installed_dir, pkg), 'a').close()
