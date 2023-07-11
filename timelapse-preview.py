#!/usr/bin/env python3

import cv2

import os
import re

def put_text(image, s, x, y):
    for line in s.splitlines():
        cv2.putText(image, line, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        cv2.putText(image, line, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        y += 12

paths = sorted([
    path
    for path in os.listdir('.')
    if re.search('(png|jpg)$', path)
])
i = 0
done = False
while not done:
    im = cv2.imread(paths[i])
    put_text(im, paths[i], 8, 18)
    cv2.imshow('timelapse-preview', im)
    k = -1
    while k == -1:
        k = cv2.waitKey(100)
        if cv2.getWindowProperty('timelapse-preview', cv2.WND_PROP_VISIBLE) < 1:
            done = True
            break
    if k in [
        ord('j'),
        83,  # right
        13,  # enter
        ord(' '),
    ]:
        i += 1
    elif k in [
        ord('k'),
        81,  # left
    ]:
        i -= 1
    elif k == 84:  # down
        i += 10
    elif k == 82:  # up
        i -= 10
    elif k == ord('l'):
        i += 100
    elif k == ord('h'):
        i -= 100
    elif k == ord(';'):
        i += 10_000
    elif k  == ord('g'):
        i -= 10_000
    i = max(0, min(len(paths)-1, i))
