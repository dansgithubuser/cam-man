import cv2
import numpy as np

class Motion:
    def __init__(
        self,
        downsample_stride=4,
        background_smoothness=10,
        diff_threshold=0.05,
        blob_stride=4,
        blob_threshold=25,
    ):
        self.downsample_stride = downsample_stride
        d = background_smoothness + 1
        self.a = background_smoothness / d
        self.b = 1 / d
        self.diff_threshold = diff_threshold
        self.blob_stride = blob_stride
        self.blob_thresh = blob_threshold
        self.im = None
        self.im_back = None
        self.im_diff = None
        self.im_gray = None
        self.im_thresh = None
        self.im_blobs = None

    def update(self, im):
        self.im = np.float32(im[::self.downsample_stride, ::self.downsample_stride]) / 256
        if self.im_back is None:
            self.im_back = self.im
        else:
            self.im_back = self.a * self.im_back + self.b * self.im
        self.im_diff = abs(self.im - self.im_back)
        self.im_gray = cv2.cvtColor(self.im_diff, cv2.COLOR_BGR2GRAY)
        _, self.im_thresh = cv2.threshold(self.im_gray, self.diff_threshold, 1, cv2.THRESH_BINARY)

    def detect(self):
        im_small = self.im_thresh[self.blob_stride//2::self.blob_stride, self.blob_stride//2::self.blob_stride]
        n_blobs = 0
        for y, row in enumerate(im_small):
            for x, pixel in enumerate(row):
                if not pixel: continue
                xi = (x + 0) * self.blob_stride
                yi = (y + 0) * self.blob_stride
                xf = (x + 1) * self.blob_stride
                yf = (y + 1) * self.blob_stride
                if cv2.countNonZero(self.im_thresh[yi:yf, xi:xf]) != self.blob_stride ** 2: continue
                n_blobs += 1
                if self.im_blobs is not None:
                    self.im_blobs[yi:yf, xi:xf] = (1, 0, 1)
        return n_blobs > self.blob_thresh

    def visualize(self, im, x=0, y=0, w=None, h=None):
        if self.im_blobs is None:
            self.im_blobs = np.zeros(self.im.shape, dtype=np.float32)
            return im
        if w == None:
            w = im.shape[1] - x
        if h == None:
            h = im.shape[0] - y
        if im.dtype != np.float32:
            if im.dtype == np.uint8:
                im = np.float32(im) / 256
            else:
                raise Exception("Don't know how to handle {im.dtype}.")
        im[y:y+h, x:x+w] += cv2.resize(
            cv2.cvtColor(self.im_thresh / 4, cv2.COLOR_GRAY2RGB),
            (w, h),
            interpolation=cv2.INTER_NEAREST,
        )
        im[y:y+h, x:x+w] += cv2.resize(
            self.im_blobs,
            (w, h),
            interpolation=cv2.INTER_NEAREST,
        )
        self.im_blobs.fill(0)
        return im
