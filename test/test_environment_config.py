#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2017-07-19 17:17:36

from src.rrsync import main
import os
import pytest


class TestSetup:

    def __init__(self, tmpdir):
        self.remote_dir = str(tmpdir.mkdir('remote'))
        self.local_dir = str(tmpdir.mkdir('local'))
        self.rrsync = Rsync_config(self.local_dir)
        self.set_up_local()
        self.set_up_remote()

    def set_up_remote(self):
        pass

    def set_up_local(self):
        self.rrsync.config["host"] = ""
        self.rrsync.config["git"] = "y"
        self.rrsync.config["remote_directory"] = self.remote_dir


@pytest.fixture()
def setup():
    return TestSetup()


def test_check_config(setup):
    setup.rrsync.make_config()
    assert setup.rrsync.check_config()


def test_make_config(setup):
    setup.rrsync.make_config()
    assert os.path.exists(os.path.join(self.local_dir, ".rsync_config"))


def test_make_input(setup):
    pass


def test_load_config(setup):
    assert setup.rrsync.load_config()


def test_config_file_path(setup):
    assert setup.rrsync.get_config_file_path


def test_configs(setup):
    assert setup.rrsync.get_configs.get("host") == ""
    assert setup.rrsync.get_configs.get("git") == "y"
    assert setup.rrsync.get_configs.get("remote_directory") == setup.remote_dir


def test_modify_config(setup):
    pass
