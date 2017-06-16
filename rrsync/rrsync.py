#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2017-06-16 14:33:27

import os
import sys
import time
import logging
import subprocess

import click
from package.environment_config import Rsync_Config
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.observers.api import DEFAULT_OBSERVER_TIMEOUT


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class COLORS(object):
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def _get_what(event):
    return 'directory' if event.is_directory else 'file'


class RSyncEventHandler(FileSystemEventHandler):
    """RSync when the events captured."""

    def __init__(self, local_path, remote_path, rsync_options=''):
        self.local_path = os.path.join(local_path)
        self.remote_path = remote_path
        self.rsync_options = rsync_options.split()
        self.rsync()

    @staticmethod
    def log(log, color):
        logging.info('{}{}{}'.format(color, log, COLORS.END))

    def on_moved(self, event):
        super(RSyncEventHandler, self).on_moved(event)

        what = _get_what(event)
        self.log(
            'Moved {}: from {} to {}'.format(
                what,
                event.src_path,
                event.dest_path
            ),
            COLORS.BLUE
        )

        self.rsync()

    def on_created(self, event):
        super(RSyncEventHandler, self).on_created(event)

        what = _get_what(event)
        self.log(
            'Created {}: {}'.format(what, event.src_path),
            COLORS.GREEN
        )

        self.rsync()

    def on_deleted(self, event):
        super(RSyncEventHandler, self).on_deleted(event)

        what = _get_what(event)
        self.log(
            'Deleted {}: {}'.format(what, event.src_path),
            COLORS.RED
        )

        self.rsync()

    def on_modified(self, event):
        super(RSyncEventHandler, self).on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        self.log(
            'Modified {}: {}'.format(what, event.src_path),
            COLORS.YELLOW
        )

        self.rsync()

    def rsync(self, relative_path=None):
        self.log('RSyncing', COLORS.PURPLE)

        local_path = self.local_path
        remote_path = self.remote_path
        if relative_path is not None:
            local_path = os.path.join(local_path, relative_path)
            remote_path = os.path.join(remote_path, relative_path)

        cmd = 'rsync -avzP {} {} {}'.format(
            ' '.join(
                self.rsync_options), local_path, remote_path
        )
        self.log(cmd, COLORS.BOLD)
        #  with open(os.devnull, 'w') as DEVNULL:
        subprocess.call(
            cmd.split(' '),
            #  stdout=DEVNULL,
            stderr=subprocess.STDOUT
        )


def send_ssh_keygen(host):
    check_subprocess('ssh-keygen')
    check_subprocess('ssh-copy-id')

    send_ssh_to_remote = click.prompt("send ssh keygen to remote?(y/n)")
    if send_ssh_to_remote == "y":
        generate_keygen = click.prompt("generate new ssh keygen?(y/n)")
        if generate_keygen == "y":
            subprocess.run(['ssh-keygen'])
        subprocess.run(['ssh-add'])
        cmd = 'ssh-copy-id {}'.format(host)
        subprocess.run(cmd.split(" "))
        click.echo("send ssh keygen finish!")


def check_subprocess(command):
    if subprocess.call(['which', str(command)]) != 0:
        print(
            COLORS.RED +
            'Can\'t find the' + str(command) + '  program, you need to install it.' +
            COLORS.END)
        sys.exit(1)


@click.command()
@click.option('--local-path', default='.', help='set the local path, default path will be\
        your current directory')
@click.option(
    '--observer-timeout',
    default=DEFAULT_OBSERVER_TIMEOUT,
    help='The observer timeout, default {}'.format(
        DEFAULT_OBSERVER_TIMEOUT
    )
)
@click.option('--rsync-options', default='', help='rsync command options')
@click.option('--modify_config', is_flag=True, help='modify rsync config')
def main(
    local_path, observer_timeout, rsync_options, modify_config
):
    rsync = Rsync_Config()
    if not rsync.check_config():
        rsync.make_config()
        send_ssh_keygen(rsync.get_configs.get("host"))
    else:
        rsync.load_config()

    if modify_config is True:
        rsync.modify_config()
        sys.exit(0)

    check_subprocess('rsync')

    remote_path = rsync.get_configs.get("host") + ":" +\
        rsync.get_configs.get("remote_directory")

    # set disable from .gitignore default
    if rsync.get_configs.get("git") == 'y':
        rsync_options += "--exclude-from=.gitignore "

    event_handler = RSyncEventHandler(local_path,
                                      remote_path,
                                      rsync_options)

    observer = Observer(timeout=observer_timeout)
    observer.schedule(event_handler, local_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
