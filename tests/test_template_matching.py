#!../interpreter/bin/python
from pathlib import Path
import sys
sys.path.append("/home/lyonbach/Repositories/pi-time-lapse")

from picamera import PiCamera
from picamera.array import PiRGBArray


import cv2
import camera_alignment as ca
import time


if __name__ == "__main__":

    resolution = (1024, 1024)
    camera = PiCamera(resolution=resolution)
    raw_capture = PiRGBArray(camera, size=resolution)
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        image = frame.array

        assertions, showcase_matrix = ca.get_alignment_info(image)
        cv2.imshow("Frame", showcase_matrix)
        key = cv2.waitKey(1) & 0xFF

        raw_capture.truncate(0)
        time.sleep(1)

        if key == ord('q'):
            break

    cv2.destroyAllWindows()

