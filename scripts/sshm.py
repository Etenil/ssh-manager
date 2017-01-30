#!/usr/bin/env python3

import sys
from sshmanager import SshManager

if __name__ == "__main__":
    sshm = SshManager()
    sshm.process(sys.argv)
