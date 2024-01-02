#!/usr/bin/env python3

import argparse
from pathlib import Path
import shutil
import time

parser = argparse.ArgumentParser()
parser.add_argument('--path', default='watchdog', help='Where to images are being stored.')
parser.add_argument('--min-disk-free-gb', type=float, default=0.5)
parser.add_argument('--max-latest-im-age-s', type=float, default=3600)
args = parser.parse_args()

#===== disk space =====#
disk_free_gb = shutil.disk_usage(args.path).free / 1e9
print(f'disk space free: {disk_free_gb:.1f} GB')

#===== latest image =====#
def latest_child(path):
    return sorted(Path(path).iterdir())[-1]

latest_im_path = latest_child(latest_child(latest_child(args.path)))
print(f'latest image is {latest_im_path}')

#===== assertions =====#
assert disk_free_gb > args.min_disk_free_gb
assert time.time() - latest_im_path.stat().st_ctime < args.max_latest_im_age_s
