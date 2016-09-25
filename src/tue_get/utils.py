import errno
import os
from argparse import Namespace
from rosdep2 import create_default_installer_context, get_default_installer, RosdepLookup
from rosdep2.main import rosdep_main
from rosdep2.rospkg_loader import DEFAULT_VIEW_KEY

from catkin_pkg.packages import find_packages
from rosdistro import get_index, get_index_url, get_cached_distribution
from rosinstall_generator.generator import generate_rosinstall_for_repos
from vcstool.commands.import_ import get_repos_in_rosinstall_format, generate_jobs
from vcstool.executor import output_repositories, execute_jobs, output_results


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_rosdistro(distroname):
    index = get_index(get_index_url())
    distro = get_cached_distribution(index, distroname)
    return distro


def update_folder(target_path, folder_mapping, verbose):
    # generate rosinstall file
    config = generate_rosinstall_for_repos(folder_mapping, version_tag=False, tar=False)

    # convert it to the vcs format
    config = get_repos_in_rosinstall_format(config)

    # update the repos
    jobs = generate_jobs(config, Namespace(path=target_path))

    print('updating %d repositories' % len(jobs))
    if verbose:
        output_repositories([job['client'] for job in jobs])

    results = execute_jobs(jobs, show_progress=True, number_of_workers=5)
    output_results(results)

    # which packages did we download?
    return {folder: find_packages(os.path.join(target_path, folder)).values() for folder in
            folder_mapping.keys()}


def install_dependencies(path):
    args = ['install', '--from-paths', path, '--ignore-src', '--as-root', 'pip:false']
    rosdep_main(args)


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
