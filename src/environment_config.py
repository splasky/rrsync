#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2017-05-29 09:54:26

import json
import os
import sys
import logging
import traceback
import click

DEFAULT_CONFIG_PATH = ".rsync_config"


class Rsync_Config(object):

    def __init__(self, path=None):
        self.config = dict()
        self.config_file_path = path
        if self.config_file_path is None:
            self.config_file_path = DEFAULT_CONFIG_PATH

    def check_config(self):
        '''check the .rsync_config is exists'''

        if not os.path.exists(self.config_file_path) or not os.path.isfile(self.config_file_path):
            return False
        if not self.load_config():
            return False
        return True

    def make_input(self):
        '''make config file input'''
        config = dict()
        click.echo("Input the rsync settings:")
        config["host"] = click.prompt(
            "ssh host ip(USER@HOST)").strip()
        config["remote_directory"] = click.prompt("remote_directory")
        config["git"] = click.prompt("Ignore files in gitignore?(y/n)").strip()

        return config

    def make_config(self):
        '''write config into file'''
        try:
            if(len(self.config) < 1):
                self.config = self.make_input()
            with open(self.config_file_path, 'w') as outfile:
                json.dump(
                    self.config, fp=outfile, separators=(',', ':'), sort_keys=True,
                )
        except:
            logging.debug(traceback.print_exc())
            sys.exit(1)

    def load_config(self):
        '''load exists .rsync_config'''
        try:
            with open(self.config_file_path, "r") as f:
                data = f.read()
                config = json.loads(data)
                self.config = dict((key, value) for key, value in config.items())
            return True
        except:
            logging.debug(traceback.print_exc())
            return False

    def print_config(self):
        print(self.config)

    @property
    def get_configs(self):
        '''get config property'''
        return self.config

    @property
    def get_config_file_path(self):
        '''get config file path'''
        return self.config_file_path

    def show_current_settings(self):
        '''show current settings'''
        self.load_config()
        click.echo("Current settings: {} ".format(self.config))

    def modify_config(self):
        '''modify config file'''
        try:
            self.show_current_settings()
            self.make_config(self.config_file_path)
            print("Change config file success.")
            return True
        except:
            return False
