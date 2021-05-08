#!../interpreter/bin/python

"""
This module tests the camera if it can take photos.
"""


from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import time


print("Testing camera...")

camera = PiCamera()
camera.rotation = 180
camera.resolution = (640, 480)
raw_capture = PiRGBArray(camera)


# Let camera warm up.
time.sleep(1)

camera.capture(raw_capture, format="bgr")
image = raw_capture.array

print("You should now see a photo.")

cv2.imshow("image", image)
cv2.waitKey(0)

cv2.destroyAllWindows()
