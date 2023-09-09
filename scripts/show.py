#!/usr/bin/env python3

import camman

import cv2

import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
parser.add_argument('--fps', type=int)
parser.add_argument('--pixel-format')
parser.add_argument('--zoom', type=float, default=1.0)
parser.add_argument('--truck', type=float, default=0.0, help='Rightward shift from center in pixels.')
parser.add_argument('--pedestal', type=float, default=0.0, help='Upward shift from center in pixels.')
args = parser.parse_args()

def file_timestamp():
    return datetime.now().astimezone().strftime('%Y-%m-%d_%H-%M-%S-%f%z')

def main():
    cam = camman.Cam(
        args.camera_index,
        args.width,
        args.height,
        args.fps,
        args.pixel_format,
    )
    window = camman.sink.Window(closeable=True)
    recording = False
    while True:
        im = cam.read()
        assert im is not None
        im = camman.im.zoom(im, args.zoom, args.truck, args.pedestal)
        c = window.update(im)
        if not window.open:
            break
        if c == ord('\r'):
            file_name = f'{file_timestamp()}.png'
            cv2.imwrite(file_name, im)
            print('saved', file_name)
        elif c == ord('r'):
            recording = not recording
            if recording:
                file_name = f'{file_timestamp()}.mkv'
                writer = cv2.VideoWriter(
                    file_name,
                    cv2.VideoWriter_fourcc(*'MJPG'),
                    cam.fps(),
                    (im.shape[1], im.shape[0]),
                )
                print(f'recording {file_name}')
            else:
                writer.release()
                print('recording finished')
        if recording:
            writer.write(im)

camman.Supervisor(main).run()
