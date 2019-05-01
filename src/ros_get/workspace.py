import logging
import os
from argparse import Namespace

import xdg
from catkin_tools.metadata import find_enclosing_workspace
from catkin_tools.terminal_color import ColorMapper
from catkin_tools.verbs import catkin_config, catkin_build
from future.moves.urllib.error import URLError
from future.moves.urllib.request import urlopen

from .utils import mkdir_p, symlink_force, __name__ as utilsname

logger = logging.getLogger(__name__)

config_dir = os.path.join(xdg.XDG_CONFIG_HOME, 'ros-get')
ws_file = os.path.join(config_dir, 'workspace')
ws_dir = os.path.join(config_dir, 'workspaces')

clr = ColorMapper().clr


def create(rosdistro_index_url, extend_path, dir, name, verbose):
    """Creates a new workspace, saves it, and switches to it if it is the first
    workspace.

    :param rosdistro_index_url: The rosdistro to use
    :param extend_path: Parent workspace to use.
    :param dir: Where to create the workspace
    :param name: Name of the new workspace.
    :param verbose: Unused.
    """

    # also allow files
    if os.path.isfile(rosdistro_index_url):
        rosdistro_index_url = 'file://%s' % os.path.realpath(rosdistro_index_url)

    try:
        urlopen(rosdistro_index_url)
    except (ValueError, URLError) as e:
        logger.error(e)
        return 1

    if not os.path.isdir(dir):
        logger.error('target path is not a directory')
        return 1

    enclosing_workspace = find_enclosing_workspace(dir)
    if enclosing_workspace:
        logger.error("Its not allowed to create a worksapce inside another workspace, other workspace found here:\n%s",
                     enclosing_workspace)
        return 1

    try:
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
    except ValueError as e:
        logger.error(e)
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
    save_config(dir, rosdistro_index_url=rosdistro_index_url)


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


def name(verbose):
    """Print name of the current workspace.

    :param verbose: Unused.
    """
    if not os.path.islink(ws_file):
        print('no current workspace found, see "ros-get ws-create --help" how to create one')
        return 1

    else:
        print(os.path.relpath(os.readlink(ws_file), 'workspaces'))


def rosdistro_url(verbose):
    ws_file = os.path.join(config_dir, 'workspace', '.ros-get')
    print(load_config(ws_file, 'rosdistro_index_url'))


def save_config(dir, **kwargs):
    ws_config_dir = os.path.join(dir, '.ros-get')
    mkdir_p(ws_config_dir)

    for k, v in kwargs.items():
        with open(os.path.join(ws_config_dir, k), 'w') as f:
            f.write(v)


def load_config(dir, key):
    ws_config_dir = os.path.join(dir, '.ros-get')
    mkdir_p(ws_config_dir)

    with open(os.path.join(dir, key)) as f:
        return f.read()
