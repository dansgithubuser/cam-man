#!/usr/bin/env python3

import camman

import cv2

import argparse
from pathlib import Path
import re

parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', default='.')
parser.add_argument('--extension', '-e', default='jpg')
parser.add_argument('--crop', nargs=4, type=int, metavar=('xi', 'yi', 'xf', 'yf'))
parser.add_argument('--resize', nargs=2, type=int, metavar=('w', 'h'))
args = parser.parse_args()

def get_paths():
    return sorted(Path(args.path).rglob(f'*.{args.extension}'))

paths = get_paths()
i = 0
done = False
while not done:
    im = cv2.imread(paths[i].as_posix())
    camman.im.put_text(im, [paths[i].name], 8, 18)
    if args.crop:
        xi, yi, xf, yf = args.crop
        im = im[yi:yf, xi:xf]
    if args.resize:
        im = cv2.resize(im, args.resize)
    cv2.imshow('timelapse-preview', im)
    k = -1
    while k == -1:
        k = cv2.waitKey(100)
        if cv2.getWindowProperty('timelapse-preview', cv2.WND_PROP_VISIBLE) < 1:
            done = True
            break
    if k in [
        ord('d'),
        ord('j'),
        83,  # right
        13,  # enter
        ord(' '),
    ]:
        i += 1
    elif k in [
        ord('s'),
        ord('k'),
        81,  # left
    ]:
        i -= 1
    elif k in [
        ord('f'),
        84,  # down
    ]:
        i += 10
    elif k in [
        ord('a'),
        82,  # up
    ]:
        i -= 10
    elif k == ord('c'):
        i += 100
    elif k == ord('x'):
        i -= 100
    elif k == ord('v'):
        i += 10_000
    elif k == ord('z'):
        i -= 10_000
    elif k == 87:  # end
        i = len(paths) - 1
    elif k == ord('r'):
        paths = get_paths()
    elif k == 27:  # escape
        break
    i = max(0, min(len(paths)-1, i))
