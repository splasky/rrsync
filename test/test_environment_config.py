#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2017-07-19 18:04:35

from src.environment_config import Rsync_Config
import os
import pytest


class TestSetup:

    def __init__(self, reomte_dir, local_dir):
        self.remote_dir = remote_dir()
        self.local_dir = local_dir()
        self.rrsync = Rsync_Config(self.local_dir)
        self.set_up_local()
        self.set_up_remote()

    def set_up_remote(self):
        pass

    def set_up_local(self):
        self.rrsync.config["host"] = ""
        self.rrsync.config["git"] = "y"
        self.rrsync.config["remote_directory"] = self.remote_dir
        self.rrsync.config_file_path = os.path.join(self. local_dir, ".rsync_config")


@pytest.fixture(scope='session')
def remote_dir(tmpdir_factory):
    return str(tmpdir_factory.mktemp('remote'))


@pytest.fixture(scope='session')
def local_dir(tmpdir_factory):
    return str(tmpdir_factory.mktemp('local'))


@pytest.fixture(scope='session')
def setup():
    return TestSetup(remote_dir, local_dir)


def test_check_config(setup):
    setup.rrsync.make_config()
    assert setup.rrsync.check_config()


def test_make_config(setup):
    setup.rrsync.make_config()
    assert os.path.exists(os.path.join(self.local_dir, ".rsync_config"))


def test_make_input(setup):
    pass


def test_load_config(setup):
    setup.rrsync.make_config()
    assert setup.rrsync.load_config()


def test_config_file_path(setup):
    assert setup.rrsync.get_config_file_path


def test_configs(setup):
    assert setup.rrsync.get_configs.get("host") == ""
    assert setup.rrsync.get_configs.get("git") == "y"
    assert setup.rrsync.get_configs.get("remote_directory") == setup.remote_dir


def test_modify_config(setup):
    pass
