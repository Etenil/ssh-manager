#!/usr/bin/env python3

import sys
if sys.version_info < (3,4):
    sys.exit('Sorry, Python < 3.4 is not supported')

from distutils.core import setup

setup(
    name='ssh-manager',
    version='0.2',
    description='SSH connections manager',
    author='Guillaume Pasquet',
    author_email='dev@etenil.net',
    url='https://github.com/Etenil/ssh-manager',
    py_modules=['sshmanager'],
    scripts=['scripts/sshm.py']
)
