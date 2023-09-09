#!/usr/bin/env python3

import camman

import cv2

import argparse
from datetime import datetime
import time

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
parser.add_argument('--pixel-format')
parser.add_argument('--delay', type=float, default=2, help='To let exposure and such configuration adjust.')
args = parser.parse_args()

def file_timestamp():
    return datetime.now().astimezone().strftime('%Y-%m-%d_%H-%M-%S-%f%z')

cam = camman.Cam(
    args.camera_index,
    args.width,
    args.height,
    None,
    args.pixel_format,
)
t0 = time.time()
while time.time() - t0 < args.delay:
    im = cam.read()
    assert im is not None
file_name = f'{file_timestamp()}.png'
cv2.imwrite(file_name, im)
print('saved', file_name)
