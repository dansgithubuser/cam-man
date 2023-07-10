#!/usr/bin/env python3

import cv2

import argparse
import datetime
import math
import os
import shutil
import time
import traceback

parser = argparse.ArgumentParser()
parser.add_argument('camera_index', nargs='?', default=0, type=int)
parser.add_argument('--period', '-p', default=1, type=int)
parser.add_argument('--width', type=int)
parser.add_argument('--height', type=int)
parser.add_argument('--extension', '-e', default='png')
parser.add_argument('--skip-similar', action='store_true')
parser.add_argument('--similarity-horizontal-sections', type=int, default=4, metavar='columns',
    help='How many sections to cut the image into horizontally - how wide is a disturbance?')
parser.add_argument('--similarity-vertical-sections', type=int, default=3, metavar='rows',
    help='How many sections to cut the image into vertically - how tall is a disturbance?')
parser.add_argument('--similarity-threshold-fit-time', type=int, default=120, metavar='periods',
    help="How long to sample the environment before fitting a threshold - what's the usual time between disturbances?")
parser.add_argument('--similarity-attention-span', type=int, default=60, metavar='periods',
    help='How long does a disturbance last?')
parser.add_argument('--similarity-max-attention-frequency', type=float, default=0.01, metavar='frequency',
    help="When to increase threshold - what's the upper bound of disturbance frequency?")
parser.add_argument('--similarity-max-time-between-images', type=int, default=300, metavar='periods',
    help='When to save an image regardless - how quick does the scene change without disturbance?')
parser.add_argument('--rm-thresh-gb', type=float, default=1, help='Remove old images when this much disk or less remains, in gigabytes.')
parser.add_argument('--rm-amount-gb', type=float, default=0.1, help='Remove this many gigabytes of images when threshold reached.')
parser.add_argument('--preview', action='store_true')
args = parser.parse_args()

class BoolHistChunk:
    def __init__(self):
        self.t = 0
        self.f = 0

    def update(self, boolean):
        if boolean:
            self.t += 1
        else:
            self.f += 1

    def size(self):
        return self.t + self.f

class BoolHist:
    def __init__(self, chunk_size, num_chunks):
        self.chunk_size = chunk_size
        self.num_chunks = num_chunks
        self.chunks = [BoolHistChunk()]

    def update(self, boolean):
        chunk = self.chunks[-1]
        chunk.update(boolean)
        if chunk.size() > self.chunk_size:
            self.chunks.append(BoolHistChunk())
        if len(self.chunks) > self.num_chunks:
            del self.chunks[0]

    def true_rate(self):
        total_size = sum(chunk.size() for chunk in self.chunks)
        if total_size < self.chunk_size:
            return 0
        return sum(chunk.t for chunk in self.chunks) / total_size

class SimilarCheckerSection:
    def __init__(self, history_size, threshold_fit_time):
        # args
        self.history_size = history_size
        self.threshold_fit_time = threshold_fit_time
        # state
        self.image_section = None
        self.d_hist = []
        self.threshold = 1.0
        self.t_to_threshold_fit = self.threshold_fit_time

    def fit_threshold(self):
        self.threshold = (self.threshold + max(self.d_hist)) / 2

    def expand_threshold(self):
        self.threshold = max(self.threshold, max(self.d_hist))

    def is_similar(self, image_section):
        assert image_section.dtype.name == 'uint8'
        # first image section
        if self.image_section is None:
            self.image_section = image_section
            return False
        # calculate difference
        d = cv2.norm(self.image_section, image_section, cv2.NORM_L1) / (image_section.size * 256)
        self.d_hist.append(d)
        if len(self.d_hist) > self.history_size:
            del self.d_hist[0]
        # compare to threshold (check if dissimilar)
        if d > self.threshold:
            self.image_section = image_section
            self.t_to_threshold_fit = self.threshold_fit_time
            return False
        # otherwise similar
        self.t_to_threshold_fit -= 1
        if self.t_to_threshold_fit <= 0:
            self.fit_threshold()
            self.t_to_threshold_fit = self.threshold_fit_time  # don't immediately refit
        return True

class SimilarChecker:
    def __init__(
        self,
        horizontal_sections,
        vertical_sections,
        threshold_fit_time,
        attention_span,
        max_attention_frequency,
        max_time_between_images,
    ):
        # args
        self.attention_span = attention_span
        self.max_attention_frequency = max_attention_frequency
        self.max_time_between_images = max_time_between_images
        # state
        self.sections = [
            [
                SimilarCheckerSection(
                    max_time_between_images,
                    threshold_fit_time,
                )
                for _ in range(horizontal_sections)
            ]
            for _ in range(vertical_sections)
        ]
        self.attention = 0
        self.attention_hist = BoolHist(max_time_between_images, 2)
        self.t_since_image = 0

    def is_similar(self, frame):
        # rein in attention frequency
        if self.attention_hist.true_rate() > self.max_attention_frequency:
            for row in self.sections:
                for section in row:
                    section.expand_threshold()
        # check if similar
        similar = True
        for row_i, row in enumerate(self.sections):
            for col_i, section in enumerate(row):
                xi = ((col_i + 0) * frame.shape[1]) // len(row)
                xf = ((col_i + 1) * frame.shape[1]) // len(row)
                yi = ((row_i + 0) * frame.shape[0]) // len(self.sections)
                yf = ((row_i + 1) * frame.shape[0]) // len(self.sections)
                similar &= section.is_similar(frame[yi:yf, xi:xf])
        # pay attention if not
        self.attention_hist.update(not similar)
        if not similar:
            self.attention = self.attention_span
            self.t_since_image = 0
            return False
        # continue paying attention
        if self.attention:
            self.attention -= 1
            self.t_since_image = 0
            return False
        # check if hit max time between images
        self.t_since_image += 1
        if self.t_since_image >= self.max_time_between_images:
            self.t_since_image = 0
            return True
        # otherwise similar
        return True

if args.skip_similar:
    similar_checker = SimilarChecker(
        args.similarity_horizontal_sections,
        args.similarity_vertical_sections,
        args.similarity_threshold_fit_time,
        args.similarity_attention_span,
        args.similarity_max_attention_frequency,
        args.similarity_max_time_between_images,
    )

def rm_old():
    if shutil.disk_usage('.').free / 1e9 > args.rm_thresh_gb: return
    for path in sorted(os.listdir('.')):
        os.remove(path)
        if shutil.disk_usage('.').free / 1e9> args.rm_thresh_gb + args.rm_amount_gb: return

def main():
    cap = cv2.VideoCapture(args.camera_index)
    if args.width: cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    if args.height: cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    while True:
        ret, frame = cap.read()
        if args.preview:
            cv2.imshow('preview', frame)
            cv2.waitKey(1)
        if not args.skip_similar or not similar_checker.is_similar(frame):
            file_name = (
                '{:%Y-%m-%b-%d_%H-%M-%S}.{}'
                .format(
                    datetime.datetime.now(),
                    args.extension,
                )
                .lower()
            )
            cv2.imwrite(file_name, frame)
        time.sleep(args.period)
        rm_old()

while True:
    try:
        main()
    except KeyboardInterrupt:
        break
    except:
        traceback.print_exc()
    time.sleep(1)
