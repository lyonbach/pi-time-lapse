from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import time

camera = PiCamera()
camera.rotation = 180

raw_capture = PiRGBArray(camera)

time.sleep(0.1)

camera.capture(raw_capture, format="bgr")
image = raw_capture.array

cv2.imshow("image", image)
cv2.waitKey(0)

cv2.destroyAllWindows()