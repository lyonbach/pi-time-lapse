#!../interpreter/bin/python

"""
This module tests the camera if it can take photos.
"""

import time

from picamera.array import PiRGBArray
from picamera import PiCamera
from fractions import Fraction

import cv2


print("Testing camera...")

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1024

camera = PiCamera()
# camera.rotation = 180

camera.resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)
raw_capture = PiRGBArray(camera)

# Set ISO to the desired value
# camera.iso = 800

# Let camera warm up.
time.sleep(2)

camera.capture(raw_capture, format="bgr")
image = raw_capture.array

print("You should now see a photo.")

cv2.imshow("Image", image)
# cv2.imwrite("test_image.png", image)
cv2.waitKey(0)

cv2.destroyAllWindows()
