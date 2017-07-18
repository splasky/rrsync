#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
# Last modified: 2017-07-19 02:07:01

from setuptools import setup, find_packages


install_requires = []
for line in open('requirements.txt', 'r'):
    install_requires.append(line.strip())

setup(
    name='rrsync',
    version='0.0.1',
    keywords=('sync', 'rsync', 'auto', 'filesystem'),
    description='Synchronize project file with remote by rsync',
    url='',
    license='MIT License',
    author='splasky',
    author_email='henrychung860326@gmail.com',
    packages=find_packages(),
    package_dir={'rrsync': 'rrsync'},
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'rrsync=src.rrsync:main'
        ]
    },
    install_requires=install_requires
)
