#!/usr/bin/env python3

import cv2

import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--background-smoothness', '-s', default=20, type=int)
parser.add_argument('--threshold', '-t', default=16, type=int)
args = parser.parse_args()

cap = cv2.VideoCapture(args.camera_index)
background = None
done = False

while not done:
    ret, frame = cap.read()
    if not ret:
        time.sleep(1)
        continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if background is None:
        background = gray
    else:
        d = args.background_smoothness + 1
        a = args.background_smoothness / d
        b = 1 / d
        background = cv2.addWeighted(background, a, gray, b, 0)
    diff = cv2.addWeighted(background, 1, gray, -1, 0)
    ret, thresh = cv2.threshold(diff, args.threshold, 255, cv2.THRESH_BINARY)
    frame = cv2.addWeighted(gray, 1, thresh, 1, 0)
    cv2.imshow('Motion', frame)
    c = cv2.waitKey(1)
    if c == 27:
        done = True
        break
