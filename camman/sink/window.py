import cv2

class Window:
    def __init__(self, title='cam-man', closeable=False):
        self.title = title
        self.closeable = closeable
        self.open = True

    def update(self, im):
        if not self.open:
            return
        cv2.imshow(self.title, im)
        c = cv2.waitKey(1)
        if self.closeable and (c == 27 or not cv2.getWindowProperty(self.title, cv2.WND_PROP_VISIBLE)):
            self.open = False
        return c
