import cv2

def put_text(
    im,
    lines,
    x,
    y,
    float_fmt='{}',
    size=0.5,
    fg_color=(255, 255, 255),
    bg_color=(0, 0, 0),
):
    for line in lines:
        if type(line) == float:
            line = float_fmt.format(line)
        else:
            line = str(line)
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

def zoom(im, zoom=1.0, truck=0, pedestal=0):
    h, w = im.shape[0:2]
    x = w / 2 + truck
    y = h / 2 - pedestal
    h /= zoom
    w /= zoom
    xi = round(x - w / 2)
    xf = round(x + w / 2) + 1
    yi = round(y - h / 2)
    yf = round(y + h / 2) + 1
    return im[yi:yf, xi:xf]
