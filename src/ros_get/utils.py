import errno
import logging
import os

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
