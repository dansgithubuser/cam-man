import cv2

import time

class Cam:
    def __init__(
        self,
        index,
        width=None,
        height=None,
        fps=None,
        outer_fps=None,
        pixel_format=None,
        **kwargs,
    ):
        self.outer_fps = outer_fps
        self.cap = cv2.VideoCapture(index, **kwargs)
        if width: self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height: self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if fps: self.cap.set(cv2.CAP_PROP_FPS, fps)
        if pixel_format: self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*pixel_format))
        self.last_read_at = time.time()

    def read(self):
        ret, im = self.cap.read()
        if self.outer_fps:
            while time.time() - self.last_read_at < 0.95 / self.outer_fps:
                ret, im = self.cap.read()
        self.last_read_at = time.time()
        if not ret:
            return None
        else:
            return im

    def fps(self):
        if self.outer_fps:
            return outer_fps
        else:
            return self.cap.get(cv2.CAP_PROP_FPS)
