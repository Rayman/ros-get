import logging
import os
from argparse import Namespace

import xdg
from catkin_tools.verbs import catkin_config, catkin_build

from .utils import mkdir_p, symlink_force, __name__ as utilsname
from catkin_tools.terminal_color import ColorMapper


logger = logging.getLogger(__name__)

config_dir = os.path.join(xdg.XDG_CONFIG_HOME, 'ros-get')
ws_file = os.path.join(config_dir, 'workspace')
ws_dir = os.path.join(config_dir, 'workspaces')

clr = ColorMapper().clr


def create(dir, extend_path, name, verbose):
    """Creates a new workspace, saves it, and switches to it if it is the first
    workspace.

    :param extend_path: Parent workspace to use.
    :param name: Name of the new workspace.
    :param verbose: Unused.
    """
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
    """Switch workspace.

    :param name: Name of the workspace to switch to.
    :param verbose: Unused.
    """
    mkdir_p(ws_dir)
    dir = os.path.join(ws_dir, name)
    if not os.path.isdir(dir):
        logger.error('workspace does not exists: %s', name)
        return 1

    logging.getLogger(utilsname).setLevel(logging.ERROR)
    symlink_force(os.path.join('workspaces', name), ws_file)


def save(dir, name, verbose):
    """Internal ws-save command to register an existing workspace.

    If there is no workspace currently, the command also switches to it.

    :param name: Name of the workspace to save.
    :param verbose: Unused.
    """
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
    """List the available workspaces.

    :param verbose: Unused.
    """
    try:
        active = os.path.relpath(os.readlink(ws_file), 'workspaces')
    except OSError:
        active = None

    mkdir_p(ws_dir)
    for link_name in os.listdir(ws_dir):
        try:
            source = os.readlink(os.path.join(ws_dir, link_name))
        except OSError as e:
            logger.error('%s => %s', link_name, repr(e))
        else:
            if link_name == active:
                print(clr('@pf-@| @{cf}%s@| => @{cf}%s@| (@{yf}active@|)') % (link_name, source))
            else:
                print(clr('@pf-@| @{cf}%s@| => @{cf}%s@|') % (link_name, source))


def locate(verbose):
    """Print location of the current workspace.

    :param verbose: Unused.
    """
    if not os.path.islink(ws_file):
        print('no current workspace found, see "ros-get ws-create --help" how to create one')
        return 1

    else:
        print(os.path.realpath(ws_file))
