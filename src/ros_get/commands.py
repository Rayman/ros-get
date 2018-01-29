import errno
import logging
import os

from catkin_pkg.packages import find_packages_allowing_duplicates
from queue import Queue, Empty
from rosdep2.main import command_update

from .utils import mkdir_p, get_rosdistro, update_folder, symlink_force, rosdep_install
from .workspace import ws_file

logger = logging.getLogger(__name__)

installed_dir = os.path.realpath(os.path.join(ws_file, '.env', 'installed'))
target_path = os.path.realpath(os.path.join(ws_file, 'repos'))
link_dir = os.path.realpath(os.path.join(ws_file, 'src'))


def install(pkgs, verbose):
    add_pkgs_to_installed_list(pkgs)
    pkgs_done = recursive_update(pkgs, verbose)
    if not pkgs_done:
        return 1
    rosdep_install(link_dir)


def update(verbose):
    logger.info('rosdep update')
    exit_code = command_update(None)

    if exit_code:
        logger.warning('rosdep exited with %d', exit_code)
        return exit_code

    pkgs = get_pkgs_from_installed_list()
    pkgs_done = recursive_update(pkgs, verbose)

    for f in os.listdir(link_dir):
        if f not in pkgs_done:
            if os.path.islink(f):
                logger.info("removing symlink: %s", f)
                os.remove(os.path.join(link_dir, f))

    rosdep_install(link_dir)


def list_installed(verbose):
    for pkg in get_pkgs_from_installed_list():
        print(pkg)


def remove(pkgs, verbose):
    remove_pkgs_from_installed_list(pkgs)
    logger.warn("marked %d package(s) for removal", len(pkgs))
    logger.warn("please run the following command to update your workspace:\n\n\tros-get update")


def recursive_update(pkgs, verbose):
    if not pkgs:
        logger.warn('no package specified')
        return set()

    # TODO: get distro from environment
    distro = get_rosdistro('kinetic')
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
                update_folder(target_path, {repo.name: repo}, verbose)

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
