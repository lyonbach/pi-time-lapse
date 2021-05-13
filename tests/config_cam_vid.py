#!../interpreter/bin/python

"""
This module tests the camera if it can take videos.
"""


import time
from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import numpy as np


print("Testing camera...")

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

resolution = (SCREEN_HEIGHT, SCREEN_WIDTH)
camera = PiCamera(resolution=resolution)
# camera.rotation = 180

raw_capture = PiRGBArray(camera, size=resolution)

# Let camera warm up.
time.sleep(1)

print("You should now see a live video.")

h_a = int(SCREEN_HEIGHT / 100 * 19)
h_t = 2

v_al = int(SCREEN_WIDTH / 1000 * 370)
v_ar = int(SCREEN_WIDTH - (SCREEN_WIDTH / 1000 * 370))
v_t = 2

for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
    image = frame.array

    # Take blue channel only for configuration purpose.
    blue = image[:, :, 0]

    # Add horizontal alignment line.
    temp = np.ones(shape=blue.shape, dtype=blue.dtype)
    temp[int(h_a - h_t/2) : int(h_a + h_t/2), :] = 0
    temp[:, int(v_al - v_t/2): int(v_al + v_t/2)] = 0
    temp[:, int(v_ar - v_t/2): int(v_ar + v_t/2)] = 0

    blue = blue * temp

    cv2.imshow("Frame", blue)
    key = cv2.waitKey(1) & 0xFF

    raw_capture.truncate(0)

    if key == ord('q'):
        break

cv2.destroyAllWindows()

