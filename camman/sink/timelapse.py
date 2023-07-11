import cv2

from datetime import datetime
from pathlib import Path

class Timelapse:
    def __init__(self, extension='png', path='.'):
        self.extension = extension
        self.path = path
        Path(path).mkdir(exist_ok=True)

    def update(self, im):
        now = datetime.now()
        file_path = '{self.path}/{:%Y-%m-%b-%d_%H-%M-%S}.{}'.format(now, self.extension).lower()
        cv2.imwrite(file_path, im)

    def rm_list(self):
        return sorted(os.listdir(self.path))
