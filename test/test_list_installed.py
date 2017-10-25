#!/usr/bin/env python
import os
import tempfile

import pytest
from mock import patch

environ_patch = None
config_home = None


def setup():
    global environ_patch, config_home
    config_home = tempfile.mkdtemp(prefix='ros-get-')

    environ_patch = patch.dict(os.environ, {'XDG_CONFIG_HOME': config_home})
    environ_patch.start()


def teardown():
    environ_patch.stop()
    # shutil.rmtree(config_home)


def test_install():
    from ros_get.commands import install
    assert install([], verbose=True) == 1


@pytest.mark.skip()
def test_update():
    from ros_get.commands import update
    assert update(verbose=True) == 1


def test_list():
    from ros_get.workspace import list_workspaces
    list_workspaces(verbose=True)


def test_remove():
    from ros_get.commands import remove
    remove(['unknown'], verbose=True)


# def test_ws_create():
#     from ros_get.workspace import create
#     create(verbose=True)


def test_ws_switch():
    from ros_get.workspace import switch
    switch('unknown', verbose=True)


def test_ws_save():
    from ros_get.workspace import save
    save('dir', 'name', verbose=True)


def test_ws_list():
    from ros_get.workspace import list_workspaces
    list_workspaces(verbose=True)


def test_ws_locate():
    from ros_get.workspace import locate
    locate(verbose=True)
