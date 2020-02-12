import errno
import logging
import os

from rosdep2.main import _rosdep_main

from rosdistro import get_index, get_index_url, repository, get_distribution, DEFAULT_INDEX_URL
from rosdistro.source_repository_specification import SourceRepositorySpecification

from rosdep2 import RosdepLookup, create_default_installer_context, get_default_installer
from rosdep2.rospkg_loader import DEFAULT_VIEW_KEY
from rosinstall_generator.generator import generate_rosinstall_for_repos
from vcstools import get_vcs_client

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

logger = logging.getLogger(__name__)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def symlink_force(source, link_name):
    logging.info("symlink '%s' => '%s'", source, link_name)
    try:
        os.symlink(source, link_name)
    except OSError as e:
        if e.errno == errno.EEXIST:
            logger.debug('symlink already exists: %s', link_name)
            logger.debug("replacing symlink from '%s' to '%s'", os.path.realpath(link_name), source)
            os.remove(link_name)
            os.symlink(source, link_name)
        else:
            raise e


class SourceRepositorySpecificationMock(SourceRepositorySpecification):
    def __init__(self, name, data):
        super(SourceRepositorySpecificationMock, self).__init__(name, data)
        self.patched_packages = data.get('packages', [])


def get_rosdistro():
    if 'ROS_DISTRO' in os.environ:
        distroname = os.environ['ROS_DISTRO']
    else:
        raise AssertionError('ROS_DISTRO is not defined in environment')

    index_url = get_index_url()
    index = get_index(index_url)

    if index_url == DEFAULT_INDEX_URL:
        logger.error('ROSDISTRO_INDEX_URL is set to the default (did you forget to source a workspace?)')
        exit(1)

    # load rosdistro with patched SourceRepositorySpecification class
    with patch.object(repository, 'SourceRepositorySpecification', SourceRepositorySpecificationMock):
        return get_distribution(index, distroname)


def update_folder(target_path, folder_mapping, restore_version, verbose):
    # generate rosinstall file
    config = generate_rosinstall_for_repos(folder_mapping, version_tag=False, tar=False)

    for i, item in enumerate(config):
        assert len(item) == 1
        repo_type, attributes = next(iter(item.items()))

        try:
            path = attributes['local-name']
        except AttributeError as e:
            logger.warning('Repository #%d does not provide the necessary ' 'information: %s' % (i, e))
            continue
        try:
            url = attributes['uri']
            if 'version' in attributes:
                version = attributes['version']
        except AttributeError as e:
            logger.warning("Repository '%s' does not provide the necessary " 'information: %s' % (path, e))
            continue

        client = get_vcs_client(repo_type, os.path.join(target_path, path))
        if client.detect_presence():
            # TODO: backup folder and checkout the new version
            if client.get_url() != url:
                logger.error("local vcs url is different from the distro's url:\n\tlocal:  %s\n\tdistro: %s",
                             client.get_url(), url)

            target_version = None
            if restore_version:
                logger.warn("Restoring %s repo %s to version %s", repo_type, path, version)
                target_version = version

            if not client.update(version=target_version, verbose=verbose):
                logger.error("Could not update %s repo: %s", repo_type, path)
                exit(1)
        else:
            assert client.checkout(url, version=version, verbose=verbose)


cached_view = None


def get_rosdep(key):
    installer_context = create_default_installer_context(verbose=False)

    installer, installer_keys, default_key, os_name, os_version = get_default_installer(
        installer_context=installer_context, verbose=False)

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
    except KeyError:
        return False


def rosdep_install(path):
    result = _rosdep_main(['install', '--from-paths', path, '-i', '-y', '--as-root', 'pip:false'])
    logger.info('rosdep exited with code %d', result)
    return result
