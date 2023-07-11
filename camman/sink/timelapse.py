import cv2

from datetime import datetime
from pathlib import Path
import time

class Timelapse:
    def __init__(self, extension='png', path='.', period=None):
        self.extension = extension
        self.path = path
        self.period = period
        self.last_save_at = None
        Path(path).mkdir(exist_ok=True)

    def update(self, im):
        now = time.time()
        if self.period != None:
            if self.last_save_at != None and now - self.last_save_at < self.period:
                return
        timestamp = datetime.now().astimezone().strftime('%Y-%m-%d_%H-%M-%S%z')
        file_path = f'{self.path}/{timestamp}.{self.extension}'
        cv2.imwrite(file_path, im)
        self.last_save_at = now

    def rm_list(self):
        return sorted(os.listdir(self.path))
