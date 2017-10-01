import errno
import logging
import os
from rosdep2 import RosdepLookup
from rosdep2 import create_default_installer_context, get_default_installer
from rosdep2.rospkg_loader import DEFAULT_VIEW_KEY

logger = logging.getLogger(__name__)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def symlink_force(target, link_name):
    try:
        os.symlink(target, link_name)
    except OSError, e:
        if e.errno == errno.EEXIST:
            logger.warn('symlink already exists: %s', link_name)
            logger.warn("replacing symlink from '%s' to '%s'", os.path.realpath(link_name), target)
            os.remove(link_name)
            os.symlink(target, link_name)
        else:
            raise e


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
    except KeyError as e:
        return False
