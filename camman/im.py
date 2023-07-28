import cv2

def put_text(
    im,
    s,
    x,
    y,
    size=0.5,
    fg_color=(255, 255, 255),
    bg_color=(0, 0, 0),
):
    for line in s.splitlines():
        cv2.putText(im, line, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, bg_color, 2)
        cv2.putText(im, line, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, fg_color, 1)
        y += 24 * size

def crop(im, top=0, bottom=0, left=0, right=0):
    if bottom:
        bottom = -bottom
    else:
        bottom = None
    if right:
        right = -right
    else:
        right = None
    return im[top:bottom, left:right]
