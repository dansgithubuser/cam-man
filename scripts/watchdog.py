#!/usr/bin/env python3

import camman

import argparse
from datetime import datetime
import time

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
parser.add_argument('--fps', type=int)
parser.add_argument('--outer-fps', type=int)
parser.add_argument('--period', type=float, default=300.0)
parser.add_argument('--motion-background-smoothness', type=float, default=10.0)
parser.add_argument('--motion-diff-threshold', type=float, default=0.15)
parser.add_argument('--motion-area-threshold', type=float, default=2500)
parser.add_argument('--attention-period', type=float, default=1.0)
parser.add_argument('--attention-span', type=float, default=5.0)
parser.add_argument('--extension', '-e', default='jpg')
parser.add_argument('--path', default='watchdog')
args = parser.parse_args()

def main():
    cam = camman.Cam(
        args.camera_index,
        args.width,
        args.height,
        args.fps,
    )
    motion_detector = camman.detector.Motion(
        args.motion_background_smoothness,
        args.motion_diff_threshold,
        args.motion_area_threshold,
    )
    window = camman.sink.Window()
    timelapse = camman.sink.Timelapse(
        args.extension,
        args.path,
        args.period,
    )
    disk_guard = camman.guard.Disk(timelapse.rm_list)
    attention_until = time.time()
    while True:
        now = time.time()
        im = cam.read()
        assert im is not None
        motion_detector.update(im)
        if motion_detector.detect():
            if now >= attention_until:
                print(datetime.now().astimezone().strftime('%Y-%m-%d_%H-%M-%S%z'), 'motion!')
            attention_until = now + args.attention_span
        if now < attention_until:
            timelapse.period = args.attention_period
        else:
            timelapse.period = args.period
        timelapse.update(im)
        disk_guard.update()
        window.update(motion_detector.visualize())

camman.Supervisor(main).run()
