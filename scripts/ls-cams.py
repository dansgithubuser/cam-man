#!/usr/bin/env python3

import subprocess

subprocess.run('v4l2-ctl --list-devices'.split())
