import cv2

import gi
gi.require_version('Gst', '1.0')  # ubuntu 22: probably `sudo apt install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good`
gi.require_version('GstRtspServer', '1.0')  # ubuntu 22: `sudo apt install libgstrtspserver-1.0-dev`
from gi.repository import GstRtspServer

class Server:
    def __init__(self):
        pass

    def update(self, im):
        pass
