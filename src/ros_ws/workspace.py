import logging
import os
import shlex
import subprocess

import xdg
from colorlog.escape_codes import escape_codes as _escape_codes

from .utils import mkdir_p, symlink_force, __name__ as utilsname

logger = logging.getLogger(__name__)

config_dir = os.path.join(xdg.XDG_CONFIG_HOME, 'ros-ws')
ws_file = os.path.join(config_dir, 'workspace')
ws_dir = os.path.join(config_dir, 'workspaces')

_cyan = _escape_codes['cyan']
_yellow = _escape_codes['yellow']
_red = _escape_codes['red']
_reset = _escape_codes['reset']


def create(extend_path, dir, name, verbose):
    """Creates a new workspace, saves it, and switches to it if it is the first
    workspace.

    :param extend_path: Parent workspace to use.
    :param dir: Where to create the workspace
    :param name: Name of the new workspace.
    :param verbose: Unused.
    """
    if not os.path.isdir(dir):
        logger.error('target path is not a directory')
        return 1

    result = create_workspace_with_colcon(extend_path, dir)

    if result:
        return result

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
            s = f'- {_cyan}{link_name}{_reset} => {_cyan}{source}{_reset}'
            if link_name == active:
                s += f' ({_yellow}active{_reset})'
            if not os.path.isdir(source):
                s += f' {_red}No such directory{_reset}'
            print(s)


def locate(verbose):
    """Print location of the current workspace.

    :param verbose: Unused.
    """
    if not os.path.islink(ws_file):
        print('no current workspace found, see "ws create --help" how to create one')
        return 1

    else:
        print(os.path.realpath(ws_file))


def name(verbose):
    """Print name of the current workspace.

    :param verbose: Unused.
    """
    if not os.path.islink(ws_file):
        print('no current workspace found, see "ws create --help" how to create one')
        return 1

    else:
        print(os.path.relpath(os.readlink(ws_file), 'workspaces'))


def create_workspace_with_colcon(extend_path, dir):
    cmd = '. %s && colcon build' % shlex.quote(os.path.join(extend_path, 'setup.sh'))
    logger.info('run: "%s"', cmd)
    result = subprocess.call(cmd, shell=True, cwd=dir, env={})
    if not result:
        return result

    # command failed, let's check if the reason
    if subprocess.call('command -v colcon', shell=True):
        logger.error("colcon was not found. Install colcon-common-extensions and try again.")
    return result
