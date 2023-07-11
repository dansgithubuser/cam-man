import cv2
import numpy as np

class Motion:
    def __init__(self, background_smoothness=10, pixel_threshold=0.05, blob_threshold=100):
        d = background_smoothness + 1
        self.a = background_smoothness / d
        self.b = 1 / d
        self.pixel_threshold = pixel_threshold
        self.blob_threshold = blob_threshold
        self.im = None
        self.im_back = None
        self.im_diff = None
        self.im_gray = None
        self.im_thresh = None
        self.blob_detector = None
        self.blob_keypoints = None

    def update(self, im):
        self.im = np.float32(im) / 256
        if self.im_back is None:
            self.im_back = self.im
        else:
            self.im_back = self.a * self.im_back + self.b * self.im
        self.im_diff = abs(self.im - self.im_back)
        self.im_gray = cv2.cvtColor(self.im_diff, cv2.COLOR_BGR2GRAY)
        _, self.im_thresh = cv2.threshold(self.im_gray, self.pixel_threshold, 1, cv2.THRESH_BINARY)

    def detect(self):
        if self.blob_detector == None:
            params = cv2.SimpleBlobDetector_Params()
            params.minThreshold = 0
            params.maxThreshold = 1
            params.minRepeatability = 1
            params.filterByArea = True
            params.minArea = self.blob_threshold
            params.filterByCircularity = False
            params.filterByConvexity = False
            params.filterByInertia = True
            params.minInertiaRatio = 0.01
            self.blob_detector = cv2.SimpleBlobDetector_create(params)
        self.blob_keypoints = self.blob_detector.detect(1 - np.uint8(self.im_thresh))
        return self.blob_keypoints

    def visualize(self):
        im = np.uint8(255 * self.im + 64 * cv2.cvtColor(self.im_thresh, cv2.COLOR_GRAY2RGB))
        if self.blob_keypoints:
            im = cv2.drawKeypoints(
                im,
                self.blob_keypoints,
                np.array([]),
                (255, 0, 255),
                cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
            )
        return im
