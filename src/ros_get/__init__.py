#!/usr/bin/env python
from __future__ import print_function

import logging
import os

# global variables
ENV_KEY = 'RG_WORKSPACE'

if ENV_KEY not in os.environ:
    path = os.path.abspath(__file__)
    path = os.path.join(os.path.dirname(path), '..', '..', 'setup.bash')
    path = os.path.normpath(path).replace(os.path.expanduser('~'), '~', 1)
    print('Please source', path)
    exit(1)

workspace = os.path.join(os.path.normpath(os.environ[ENV_KEY]), '')
installed_dir = os.path.join(workspace, '.env', 'installed', '')
target_path = os.path.join(workspace, 'src', '')
link_dir = os.path.join('..', 'src_link', '')


def log_workspace():
    logger = logging.getLogger(__name__)
    logger.debug('Workspace config:')
    logger.debug('\tworkspace: %s', workspace)
    logger.debug('\tinstalled_dir: %s', installed_dir)
    logger.debug('\ttarget_path: %s', target_path)
    logger.debug('\tlink_dir: %s', link_dir)
