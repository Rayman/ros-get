#!/usr/bin/env python
from __future__ import print_function

import logging
import os
from argparse import Namespace

from catkin_tools.verbs import catkin_config, catkin_build

from . import config_dir

logger = logging.getLogger(__name__)

ws_file = os.path.join(config_dir, 'workspace')
ws_dir = os.path.join(config_dir, 'workspaces')


def create(dir, extend_path, verbose):
    if not os.path.isdir(dir):
        print('target path is not a directory')
        return

    if catkin_config.main(
        Namespace(
            workspace=dir,
            extend_path=extend_path,
            profile=None,
            append_args=None,
            remove_args=None,
            init=True,
            mkdirs=True)):
        logger.error('catkin config error')
        exit(1)

    if catkin_build.main(
        Namespace(
            workspace=dir,
            develdebug=None,
            force_color=None,
            no_color=None,
            build_this=None,
            start_with_this=None,
            no_deps=None,
            profile=None,
            mem_limit=None,
            dry_run=None,
            get_env=None,
            save_config=None,
            parallel_jobs=None,
            verbose=None,
            packages=None,
            start_with=None,
            unbuilt=None,
            force_cmake=None,
            pre_clean=None,
            interleave_output=None,
            no_status=None,
            limit_status_rate=10.0,
            no_install_lock=None,
            no_notify=None,
            continue_on_failure=None,
            summarize=None,
        )):
        logger.error('catkin build error')
        exit(1)


def switch(verbose):
    pass
