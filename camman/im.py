def put_text(
    frame,
    s,
    x,
    y,
    size=0.5,
    fg_color=(255, 255, 255),
    bg_color=(0, 0, 0),
):
    for line in s.splitlines():
        cv2.putText(frame, line, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, bg_color, 2)
        cv2.putText(frame, line, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, fg_color, 1)
        y += 24 * size
