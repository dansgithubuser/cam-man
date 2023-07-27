#!/usr/bin/env python3

import camman

import argparse
from datetime import datetime
import time

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int, help='Which camera to use, 0 for "/dev/video0".')
parser.add_argument('--width', type=int, help='Width in pixels to request from the camera.')
parser.add_argument('--height', type=int, help='Height in pixels to request from the camera.')
parser.add_argument('--ignore-top', type=int, default=0, help='Pixels from the top to ignore in motion detection.')
parser.add_argument('--ignore-bottom', type=int, default=0, help='Pixels from the bottom to ignore in motion detection.')
parser.add_argument('--ignore-left', type=int, default=0, help='Pixels from the left to ignore in motion detection.')
parser.add_argument('--ignore-right', type=int, default=0, help='Pixels from the right to ignore in motion detection.')
parser.add_argument('--fps', type=int, help='Frames per second to request from the camera.')
parser.add_argument('--outer-fps', type=int, help='Frames per second to send for motion detection and saving to disk.')
parser.add_argument('--period', type=float, default=300.0, help='How often to save an image normally.')
parser.add_argument('--motion-background-smoothness', type=float, default=10.0, help='How slowly the estimated background changes.')
parser.add_argument('--motion-diff-threshold', type=float, default=0.15, help='How much change is considered motion per pixel, grayscale 0-1.')
parser.add_argument('--motion-blob-stride', type=int, default=4, help='Side length of a square blob in pixels.')
parser.add_argument('--motion-blob-threshold', type=int, default=25, help='How many blobs should be in motion to start paying attention.')
parser.add_argument('--attention-period', type=float, default=1.0, help='How often to save an image when paying attention.')
parser.add_argument('--attention-span', type=float, default=5.0, help='How long attention should last.')
parser.add_argument('--extension', '-e', default='jpg', help='Image file extension to use, default "jpg".')
parser.add_argument('--path', default='watchdog', help='Where to store images.')
parser.add_argument('--preview', action='store_true', help='Open a window showing what is going on.')
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
        args.motion_blob_stride,
        args.motion_blob_threshold,
    )
    if args.preview:
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
        im_crop = camman.im.crop(im, args.ignore_top, args.ignore_bottom, args.ignore_left, args.ignore_right)
        motion_detector.update(im_crop)
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
        if args.preview:
            window.update(motion_detector.visualize(im, args.ignore_left, args.ignore_top))

camman.Supervisor(main).run()
