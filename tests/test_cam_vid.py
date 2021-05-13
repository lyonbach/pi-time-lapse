#!../interpreter/bin/python

"""
This module tests the camera if it can take videos.
"""


from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import time


print("Testing camera...")

resolution = (640, 640)
camera = PiCamera(resolution=resolution)
# camera.rotation = 180

raw_capture = PiRGBArray(camera, size=resolution)

# Let camera warm up.
time.sleep(1)

print("You should now see a live video.")

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array

    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    raw_capture.truncate(0)

    if key == ord('q'):
        break

cv2.destroyAllWindows()

