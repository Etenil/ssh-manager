#!/usr/bin/env python

import sys
from sshmanager import SshManager

if __name__ == "__main__":
    sshm = SshManager()
    sshm.process(sys.argv)
