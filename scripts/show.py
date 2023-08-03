#!/usr/bin/env python3

import camman

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
parser.add_argument('--fps', type=int)
parser.add_argument('--pixel-format')
args = parser.parse_args()

def main():
    cam = camman.Cam(
        args.camera_index,
        args.width,
        args.height,
        args.fps,
        args.pixel_format,
    )
    window = camman.sink.Window(closeable=True)
    while True:
        im = cam.read()
        assert im is not None
        window.update(im)
        if not window.open:
            break

camman.Supervisor(main).run()
