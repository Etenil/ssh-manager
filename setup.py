#!/usr/bin/env python

from distutils.core import setup

setup(
    name='ssh-manager',
    version='0.1',
    description='SSH connections manager',
    author='Guillaume Pasquet',
    author_email='dev@etenil.net',
    url='https://github.com/Etenil/ssh-manager',
    py_modules=['sshmanager'],
    scripts=['scripts/sshm.py']
)