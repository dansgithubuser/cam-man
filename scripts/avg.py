#!/usr/bin/env python3

import camman

import cv2
import numpy as np

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
parser.add_argument('--fps', type=int)
parser.add_argument('--pixel-format')
parser.add_argument('--number-of-pics', '-n', type=int, default=10)
args = parser.parse_args()

def main():
    cam = camman.Cam(
        args.camera_index,
        width=args.width,
        height=args.height,
        fps=args.fps,
        pixel_format=args.pixel_format,
    )
    im_sum = None
    for i in range(args.number_of_pics):
        im = cam.read()
        assert im is not None
        im = np.float32(im)
        if im_sum is None:
            im_sum = im
        else:
            im_sum += im
    return im_sum

im_sum = camman.Supervisor(main).run()

im_sum /= args.number_of_pics
cv2.imwrite(f'avg.png', im_sum)
