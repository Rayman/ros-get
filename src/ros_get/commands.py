#!/usr/bin/env python
from __future__ import print_function

import logging
import os

from .utils import mkdir_p
from .workspace import ws_file

logger = logging.getLogger(__name__)
installed_dir = os.path.join(ws_file, '.env', 'installed')
target_path = os.path.join(ws_file, 'src')


def install(pkgs, verbose):
    pkgs_queue = list(pkgs)
    print('TODO: %s' % pkgs)


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
