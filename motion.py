#!/usr/bin/env python3

import cv2
import numpy as np

import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--background-smoothness', '-s', default=10, type=int)
parser.add_argument('--threshold', '-t', default=0.05, type=float)
args = parser.parse_args()

cap = cv2.VideoCapture(args.camera_index)
background = None
done = False

while not done:
    ret, frame = cap.read()
    frame = np.float32(frame) / 256
    if not ret:
        time.sleep(1)
        continue
    if background is None:
        background = frame
    else:
        d = args.background_smoothness + 1
        a = args.background_smoothness / d
        b = 1 / d
        background = a * background + b * frame
    diff = abs(frame - background)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, args.threshold, 1, cv2.THRESH_BINARY)
    color = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
    frame += color
    cv2.imshow('Motion', frame)
    c = cv2.waitKey(1)
    if c == 27:
        done = True
        break
