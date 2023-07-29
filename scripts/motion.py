#!/usr/bin/env python3

import camman

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
parser.add_argument('--downsample-stride', default=4, type=int)
parser.add_argument('--background-smoothness', '-s', default=10.0, type=float)
parser.add_argument('--diff-threshold', '--dt', default=0.05, type=float)
args = parser.parse_args()

cam = camman.Cam(
    args.camera_index,
    args.width,
    args.height,
)
motion_detector = camman.detector.Motion(
    args.downsample_stride,
    args.background_smoothness,
    args.diff_threshold,
)
window = camman.sink.Window(closeable=True)

while True:
    im = cam.read()
    motion_detector.update(im)
    motion_detector.detect()
    im = motion_detector.visualize(im)
    window.update(im)
    if not window.open:
        break
