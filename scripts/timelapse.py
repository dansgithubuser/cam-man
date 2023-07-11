#!/usr/bin/env python3

import camman

import argparse
from datetime import datetime
import time

TIMESTAMP = datetime.now().astimezone().strftime('%Y-%m-%d_%H-%M-%S%z')

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--period', '-p', default=1, type=int)
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
parser.add_argument('--extension', '-e', default='png')
parser.add_argument('--path', default=f'timelapse-{TIMESTAMP}')
args = parser.parse_args()

def main():
    cam = camman.Cam(args.camera_index, args.width, args.height)
    window = camman.sink.Window()
    timelapse = camman.sink.Timelapse(args.extension, args.path)
    while True:
        im = cam.read()
        assert im is not None
        window.update(im)
        timelapse.update(im)
        time.sleep(args.period)

camman.Supervisor(main).run()
