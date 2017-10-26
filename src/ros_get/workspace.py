#!/usr/bin/env python


import logging
import os
from argparse import Namespace
from catkin_tools.verbs import catkin_config, catkin_build

from ros_get.utils import mkdir_p, symlink_force

from . import config_dir

logger = logging.getLogger(__name__)

ws_file = os.path.join(config_dir, 'workspace')
ws_dir = os.path.join(config_dir, 'workspaces')


def create(dir, extend_path, name, verbose):
    if not os.path.isdir(dir):
        logger.error('target path is not a directory')
        return 1

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
        return 1

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
                summarize=None)):
        logger.error('catkin build error')
        return 1

    save(dir, name, verbose)


def switch(name, verbose):
    dir = os.path.join(ws_dir, name)
    if not os.path.isdir(dir):
        logger.error('workspace does not exists: %s', name)
        return 1

    mkdir_p(ws_dir)

    logging.getLogger('ros_get.utils').setLevel(logging.ERROR)
    symlink_force(os.path.join('workspaces', name), ws_file)


def save(dir, name, verbose):
    if not os.path.isdir(dir):
        logger.error('target path is not a directory')
        return 1

    abs_dir = os.path.abspath(dir)
    if not name:
        name = os.path.basename(abs_dir)

    if not name:
        logger.error('name not valid: %s', name)
        return 1

    # save the result
    mkdir_p(ws_dir)
    symlink_force(abs_dir, os.path.join(ws_dir, name))
    logger.info("saved the workspace as '%s'", name)

    if not os.path.islink(ws_file):
        logger.info("created first workspace, let's make it the default")
        switch(name, verbose)


def list_workspaces(verbose):
    mkdir_p(ws_dir)
    for link_name in os.listdir(ws_dir):
        try:
            source = os.readlink(os.path.join(ws_dir, link_name))
        except OSError as e:
            logger.error('%s => %s', link_name, repr(e))
        else:
            print('%s => %s' % (link_name, source))


def locate(verbose):
    print(os.path.realpath(ws_file))
