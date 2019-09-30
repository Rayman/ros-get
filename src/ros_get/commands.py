import errno
import logging
import os
from argparse import Namespace

from catkin_pkg.packages import find_packages_allowing_duplicates
from queue import Queue, Empty
from rosdep2.main import command_update
from rosinstall_generator.generator import generate_rosinstall_for_repos
from vcstools import get_vcs_client

from .utils import mkdir_p, get_rosdistro, update_folder, symlink_force, rosdep_install
from .workspace import ws_file

logger = logging.getLogger(__name__)

installed_dir = os.path.realpath(os.path.join(ws_file, '.env', 'installed'))
target_path = os.path.realpath(os.path.join(ws_file, 'repos'))
link_dir = os.path.realpath(os.path.join(ws_file, 'src'))


def install(pkgs, verbose):
    pkgs_done = recursive_update(pkgs, False, verbose)
    pkgs_succeeded = [pkg for pkg in pkgs if pkg in pkgs_done]
    pkgs_skipped = set(pkgs) - pkgs_done

    for pkg in pkgs_skipped:
        logger.error("Package %s was not defined in the ros distribution", pkg)
    add_pkgs_to_installed_list(pkgs_succeeded)

    if not pkgs_done:
        return 1
    result = rosdep_install(link_dir)
    if pkgs_skipped:
        return 1
    return result


def update(restore_versions, verbose):
    # first check if a custom rosdistro has been configured
    get_rosdistro()

    logger.info('rosdep update')
    exit_code = command_update(Namespace(include_eol_distros=False))
    if exit_code:
        logger.error('`rosdep update` exited with %d', exit_code)
        return exit_code

    pkgs = get_pkgs_from_installed_list()
    pkgs_done = recursive_update(pkgs, restore_versions, verbose)

    cleanup_symlinks(pkgs_done)

    exit_code = rosdep_install(link_dir)
    if exit_code:
        logger.error('`rosdep install` exited with %d', exit_code)
        return exit_code


def status(verbose):
    distro = get_rosdistro()

    repositories = [
        r for r in distro.repositories.values() if r.source_repository and r.source_repository.patched_packages
    ]

    for path in os.listdir(target_path):
        name = os.path.basename(path)

        repo = [r for r in repositories if r.name == name]

        if len(repo) != 1:
            logger.warning('skipping unknown repo: %s', name)
            continue
        repo = repo[0]

        config = generate_rosinstall_for_repos({'DOESNOTMATTER': repo}, version_tag=False, tar=False)[0]

        assert len(config) == 1
        repo_type, attributes = next(iter(config.items()))

        try:
            url = attributes['uri']
            if 'version' in attributes:
                version = attributes['version']
        except AttributeError as e:
            logger.warning("Repository '%s' does not provide the necessary " 'information: %s' % (path, e))
            continue

        client = get_vcs_client(repo_type, os.path.join(target_path, path))

        if client.get_url() != url:
            logger.error("local vcs url is different from the distro's url:\n\tlocal:  %s\n\tdistro: %s",
                         client.get_url(), url)

        current_version = client.get_current_version_label()
        if current_version == version:
            print('=== %s (%s) ===' % (name, repo_type))
        else:
            print('=== %s (%s) === @ %s' % (name, repo_type, current_version))

        print(client.get_status(untracked=True))


def list_packages(installed, verbose):
    if installed:
        for pkg in sorted(get_pkgs_from_installed_list()):
            print(pkg)
    else:
        distro = get_rosdistro()

        pkgs = []
        for r in distro.repositories.values():
            if r.source_repository and r.source_repository.patched_packages:
                for p in r.source_repository.patched_packages:
                    pkgs.append(p)

        for p in sorted(pkgs):
            print(p)


def remove(pkgs, verbose):
    remove_pkgs_from_installed_list(pkgs)
    logger.warn("marked %d package(s) for removal", len(pkgs))
    logger.warn("please run the following command to update your workspace:\n\n\tros-get update")


def recursive_update(pkgs, restore_versions, verbose):
    if not pkgs:
        logger.warn('no package specified')
        return set()

    distro = get_rosdistro()

    repositories = [
        r for r in distro.repositories.values() if r.source_repository and r.source_repository.patched_packages
    ]

    pkgs_queue = Queue()
    pkgs_done = set()
    for pkg in pkgs:
        pkgs_queue.put_nowait(pkg)

    # mapping from manifest to found location
    pkgs_manifests = {}

    try:
        while True:
            pkg = pkgs_queue.get_nowait()

            if pkg in pkgs_done:
                continue

            repo = [repo for repo in repositories if pkg in repo.source_repository.patched_packages]
            if len(repo) == 0:
                logger.debug("Package '%s' can't be found in a repository", pkg)
                continue

            assert len(repo) == 1, "Package '%s' is in multiple repositories" % pkg
            repo = repo[0]

            logger.info('installing: %s', pkg)
            if not len([m for m in pkgs_manifests if m.name == pkg]):
                update_folder(target_path, {repo.name: repo}, restore_versions, verbose)

                # which packages did we download?
                updated_packages = find_packages_allowing_duplicates(os.path.join(target_path, repo.name))

                # first check for expected packages that were not found
                found_names = set(package.name for package in updated_packages.values())
                for package in repo.source_repository.patched_packages:
                    if package not in found_names:
                        logger.warning("Package '%s' not found in the repo: '%s'", package, repo.name)

                # then check for found packages that were not in the yaml
                for subfolder, package in updated_packages.items():
                    if package.name in repo.source_repository.patched_packages:
                        logger.info("found '%s'" % os.path.join(repo.name, subfolder))
                        pkgs_manifests[package] = os.path.join(repo.name, subfolder)
                    else:
                        logger.debug("Found package '%s' in an unexpected repo: '%s'", package.name, repo.name)

            manifest = [m for m in pkgs_manifests if m.name == pkg]
            if not len(manifest):
                logger.error("Required package '%s' not found", pkg)
                exit(1)
            assert len(manifest) == 1, "Package '%s' was found multiple times" % pkg
            manifest = manifest[0]

            deps = manifest.buildtool_depends + manifest.build_depends + manifest.run_depends + manifest.test_depends
            for dep in deps:
                if dep not in pkgs_done:
                    logger.debug("queing: '%s'", dep.name)
                    pkgs_queue.put_nowait(dep.name)

            pkgs_done.add(pkg)

    except Empty:
        pass

    if not pkgs_done:
        logger.error('no repository updated, package could not be found')

    # create the symlinks in the src folder
    for pkg in pkgs_done:
        manifest = [m for m in pkgs_manifests if m.name == pkg]
        assert len(manifest) == 1
        manifest = manifest[0]

        folder = pkgs_manifests[manifest]

        source = os.path.join(target_path, folder)
        link_name = os.path.join(link_dir, manifest.name)

        source = os.path.relpath(source, link_dir)
        symlink_force(source, link_name)

    return pkgs_done


def cleanup_symlinks(pkgs_done):
    """Remove all symlinks from the link_dir that are not in pkgs_done"""
    logger.info("Cleaning up old symlinks")
    for f in os.listdir(link_dir):
        if f not in pkgs_done:
            filename = os.path.join(link_dir, f)
            if os.path.islink(filename):
                logger.info("removing symlink: %s", f)
                os.remove(filename)


def add_pkgs_to_installed_list(pkgs):
    mkdir_p(installed_dir)

    # touch the file
    for pkg in pkgs:
        logger.debug('marking for installation: %s', pkg)
        open(os.path.join(installed_dir, pkg), 'a').close()


def get_pkgs_from_installed_list():
    mkdir_p(installed_dir)
    return os.listdir(installed_dir)


def remove_pkgs_from_installed_list(pkgs):
    for pkg in pkgs:
        try:
            os.remove(os.path.join(installed_dir, pkg))
        except OSError as e:
            if e.errno == errno.ENOENT:
                logger.error('unable to locate package: %s', pkg)
            else:
                raise
        else:
            logger.info('Removing: %s', pkg)
