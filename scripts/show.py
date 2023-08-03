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
parser.add_argument('--zoom', type=float, default=1.0)
parser.add_argument('--truck', type=float, default=0.0, help='Rightward shift from center in pixels.')
parser.add_argument('--pedestal', type=float, default=0.0, help='Upward shift from center in pixels.')
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
        im = camman.im.zoom(im, args.zoom, args.truck, args.pedestal)
        window.update(im)
        if not window.open:
            break

camman.Supervisor(main).run()
