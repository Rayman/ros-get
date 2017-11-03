import errno
import logging
import os
from argparse import Namespace
from rosdistro import get_index, get_index_url, repository, get_distribution
from rosdistro.source_repository_specification import SourceRepositorySpecification

from mock import patch
from rosdep2 import RosdepLookup, create_default_installer_context, get_default_installer
from rosdep2.rospkg_loader import DEFAULT_VIEW_KEY
from rosinstall_generator.generator import generate_rosinstall_for_repos
from vcstool.commands.import_ import get_repos_in_rosinstall_format, generate_jobs
from vcstool.executor import output_repositories, execute_jobs, output_results

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


def get_rosdistro(distroname):
    index = get_index(get_index_url())

    # load rosdistro with patched SourceRepositorySpecification class
    with patch.object(repository, 'SourceRepositorySpecification', SourceRepositorySpecificationMock):
        return get_distribution(index, distroname)


def update_folder(target_path, folder_mapping, verbose):
    # generate rosinstall file
    config = generate_rosinstall_for_repos(folder_mapping, version_tag=False, tar=False)

    # convert it to the vcs format
    config = get_repos_in_rosinstall_format(config)

    # update the repos
    jobs = generate_jobs(config, Namespace(path=target_path, force=False, retry=False))

    if verbose:
        output_repositories([job['client'] for job in jobs])

    results = execute_jobs(jobs, show_progress=True, number_of_workers=5)
    output_results(results)


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
