#!/usr/bin/env python3

import camman

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--background-smoothness', '-s', default=10, type=int)
parser.add_argument('--threshold', '-t', default=0.05, type=float)
args = parser.parse_args()

cam = camman.Cam(args.camera_index)
motion_detector = camman.detector.Motion(args.background_smoothness, args.threshold)
window = camman.sink.Window(closeable=True)

while True:
    im = cam.read()
    motion_detector.update(im)
    window.update(motion_detector.visualize())
    if not window.open:
        break
