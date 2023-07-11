import cv2

class Window:
    def __init__(self, title='cam-man'):
        self.title = title
        self.open = True

    def update(self, im):
        if not self.open:
            return
        cv2.imshow(self.title, im)
        c = cv2.waitKey(1)
        if c == 27:
            self.open = False
