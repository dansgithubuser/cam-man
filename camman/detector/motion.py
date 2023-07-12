import cv2
import numpy as np

class Motion:
    def __init__(self, background_smoothness=10, diff_threshold=0.05, area_threshold=100):
        d = background_smoothness + 1
        self.a = background_smoothness / d
        self.b = 1 / d
        self.diff_threshold = diff_threshold
        self.area_threshold = area_threshold
        self.im = None
        self.im_back = None
        self.im_diff = None
        self.im_gray = None
        self.im_thresh = None
        self.contours = None

    def update(self, im):
        self.im = np.float32(im) / 256
        if self.im_back is None:
            self.im_back = self.im
        else:
            self.im_back = self.a * self.im_back + self.b * self.im
        self.im_diff = abs(self.im - self.im_back)
        self.im_gray = cv2.cvtColor(self.im_diff, cv2.COLOR_BGR2GRAY)
        _, self.im_thresh = cv2.threshold(self.im_gray, self.diff_threshold, 1, cv2.THRESH_BINARY)

    def detect(self):
        contours, hierarchy = cv2.findContours(np.uint8(self.im_thresh), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = [(i, cv2.contourArea(i)) for i in contours]
        contours = [i for i in contours if i[1] > self.area_threshold]
        self.contours = contours
        print(sum(i[1] for i in contours))
        return

    def visualize(self):
        im = np.uint8(255 * self.im + 64 * cv2.cvtColor(self.im_thresh, cv2.COLOR_GRAY2RGB))
        im = self.im + cv2.cvtColor(self.im_thresh, cv2.COLOR_GRAY2RGB) / 2
        if self.contours:
            cv2.drawContours(
                im,
                [i[0] for i in self.contours],
                -1,
                (1.0, 0.0, 1.0),
            )
        return im
