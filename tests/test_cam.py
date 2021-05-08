#!../interpreter/bin/python

"""
This module tests the camera if it can take photos.
"""


from picamera.array import PiRGBArray
from picamera import PiCamera
from fractions import Fraction

import cv2
import time


print("Testing camera...")

camera = PiCamera()
camera.rotation = 180
camera.resolution = (640, 480)
raw_capture = PiRGBArray(camera)


# Let camera warm up.

# Set ISO to the desired value
camera.iso = 800
# Wait for the automatic gain control to settle
time.sleep(5)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

camera.capture(raw_capture, format="bgr")
image = raw_capture.array

print("You should now see a photo.")

cv2.imshow("image", image)
cv2.waitKey(0)

cv2.destroyAllWindows()
