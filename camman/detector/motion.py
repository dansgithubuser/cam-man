import cv2
import numpy as np

class Motion:
    def __init__(self, background_smoothness=10, threshold=0.05):
        d = background_smoothness + 1
        self.a = background_smoothness / d
        self.b = 1 / d
        self.threshold = threshold
        self.im = None
        self.im_back = None
        self.im_diff = None
        self.im_gray = None
        self.im_thresh = None

    def update(self, im):
        self.im = np.float32(im) / 256
        if self.im_back is None:
            self.im_back = self.im
        else:
            self.im_back = self.a * self.im_back + self.b * self.im
        self.im_diff = abs(self.im - self.im_back)
        self.im_gray = cv2.cvtColor(self.im_diff, cv2.COLOR_BGR2GRAY)
        _, self.im_thresh = cv2.threshold(self.im_gray, self.threshold, 1, cv2.THRESH_BINARY)

    def visualize(self):
        return self.im + cv2.cvtColor(self.im_thresh, cv2.COLOR_GRAY2RGB)
