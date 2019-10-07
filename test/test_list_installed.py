import imp

import pytest
import ros_get.workspace
import xdg
from ros_get import create, install, list_workspaces, locate, remove, save, switch, update


@pytest.fixture()
def empty_config_home(tmpdir, monkeypatch):
    """
    Monkeypatch XDG_CONFIG_HOME to an empty directory in /tmp
    """
    monkeypatch.setenv('XDG_CONFIG_HOME', str(tmpdir))
    imp.reload(xdg)
    imp.reload(ros_get.workspace)
    return tmpdir


def test_fixture(empty_config_home):
    assert ros_get.workspace.config_dir.startswith('/tmp')


def test_install(empty_config_home):
    assert install([], verbose=True) == 1


@pytest.mark.skip()
def test_update():
    assert update(restore_versions=False, verbose=True) == 1


def test_list(empty_config_home):
    list_workspaces(verbose=True)


def test_remove(empty_config_home):
    remove(['unknown'], verbose=True)


@pytest.mark.skip()
def test_ws_create(empty_config_home):
    # TODO: implement when the final implementation of create is finished
    create(verbose=True)


def test_ws_switch(empty_config_home):
    switch('unknown', verbose=True)


def test_ws_save(empty_config_home):
    save('dir', 'name', verbose=True)


def test_ws_list(empty_config_home):
    assert len(empty_config_home.listdir()) == 0

    list_workspaces(verbose=True)

    config = empty_config_home.join('ros-get')
    assert config.check(dir=1)
    assert config.join('workspace').check(exists=0)
    assert config.join('workspaces').check(dir=1)


def test_ws_locate(empty_config_home):
    locate(verbose=True)
    assert len(empty_config_home.listdir()) == 0
