#!/usr/bin/env python3

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('device', nargs='?', default='0')
args = parser.parse_args()

subprocess.run(f'v4l2-ctl -d {args.device} --list-formats-ext'.split())
