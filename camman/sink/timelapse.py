import cv2

from datetime import datetime
import os
from pathlib import Path
import threading
import time

class Timelapse:
    def __init__(self, extension='png', path='.', period=None, context_duration=None):
        self.extension = extension
        self.path = Path(path)
        self.period = period
        self.context_duration = context_duration
        self.last_save_at = None
        self.context = []
        Path(path).mkdir(exist_ok=True)

    def update(self, im):
        now = time.time()
        # skip if it's not time to save
        if self.period != None:
            if self.last_save_at != None and now - self.last_save_at < self.period:
                # keep context
                if self.context_duration:
                    self.context.append((im, now))
                    while self.context and now - self.context[0][1] > self.context_duration:
                        del self.context[0]
                # done
                return
        # save
        self.save(im, now)
        self.last_save_at = now

    def save(self, im, t):
        dt = datetime.fromtimestamp(t).astimezone()
        y = dt.strftime('%Y')
        ymd = dt.strftime('%Y-%m-%d')
        timestamp = dt.strftime('%Y-%m-%d_%H-%M-%S.%f%z')
        file_path = self.path / y / ymd / f'{timestamp}.{self.extension}'
        file_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(file_path.as_posix(), im)

    def save_context(self):
        context = self.context
        self.context = []
        threading.Thread(target=lambda: [self.save(im, t) for im, t in context]).start()

    def rm_list(self):
        return sorted(self.path.rglob('*'))
