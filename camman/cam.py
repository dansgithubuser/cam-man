import cv2

class Cam:
    def __init__(
        self,
        index,
        width=None,
        height=None,
        fps=None,
        pixel_format=None,
        **kwargs,
    ):
        self.cap = cv2.VideoCapture(index, **kwargs)
        if width: self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        if height: self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if fps: self.cap.set(cv2.CAP_PROP_FPS, fps)
        if pixel_format: self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*pixel_format))

    def read(self):
        ret, im = self.cap.read()
        if not ret:
            return None
        else:
            return im
