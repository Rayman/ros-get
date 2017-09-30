import errno
import logging
import os

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
