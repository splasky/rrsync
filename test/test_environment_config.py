#! /usr/bin/python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2017-07-20 11:25:26

from src.environment_config import Rsync_Config
import unittest
import tempfile
import shutil
import os
import pytest


class TestEnvironmentConfig(unittest.TestCase):

    def setUp(self):
        self.remote_dir = tempfile.mkdtemp()
        self.local_dir = tempfile.mkdtemp()
        self.rrsync = Rsync_Config(self.local_dir)
        self.set_up_local()
        self.set_up_remote()

    def tearDown(self):
        shutil.rmtree(self.remote_dir)
        shutil.rmtree(self.local_dir)

    def set_up_remote(self):
        pass

    def set_up_local(self):
        self.rrsync.config["host"] = ""
        self.rrsync.config["git"] = "y"
        self.rrsync.config["remote_directory"] = self.remote_dir
        self.rrsync.config_file_path = os.path.join(self.local_dir, ".rsync_config")

    def test_check_config(self):
        self.rrsync.make_config()
        assert self.rrsync.check_config()

    def test_make_config(self):
        self.rrsync.make_config()
        assert os.path.exists(os.path.join(self.local_dir, ".rsync_config"))

    def test_make_input(self):
        pass

    def test_load_config(self):
        self.rrsync.make_config()
        assert self.rrsync.load_config()

    def test_config_file_path(self):
        assert self.rrsync.get_config_file_path

    def test_configs(self):
        assert self.rrsync.get_configs.get("host") == ""
        assert self.rrsync.get_configs.get("git") == "y"
        assert self.rrsync.get_configs.get("remote_directory") == self.remote_dir

    def test_modify_config(self):
        pass
