import datetime
from pathlib import Path
import time
import picam_flash

import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

OUTPUT_EXTENSION = ".png"

# TODO: ADD "DO UNTIL" FUNCTIONALITY
# TODO: ADD LOGGING

class TimeLapseWorker:

    def __init__(self, interval: int, output_folder: str, photo_count_limit: int=None):

        """
        :interval     : Time (seconds) to wait until next shot.
        :output_folder: Folder to save the shots to.
        """

        self._interval = interval

        # Check if output folder exists.
        self._output_folder = Path(output_folder)
        if not self._output_folder.is_dir():
            raise IOError("Given target folder does not exist!")

        self._photo_count_limit = photo_count_limit or float("inf")

        # We initialize total shoot count to the number of photos in the given output folder.
        self._total_shot_count = len(list(self._output_folder.glob(f"*{OUTPUT_EXTENSION}")))
        self.__last_shot_time = None
        self.__camera = PiCamera()

    def _set_options(self):

        self.__camera.resolution = (1024, 1024)
#        self.__camera.rotation = 180

        # Set ISO to the desired value
#        self.__camera.iso = 800
        time.sleep(15)
        # Wait for the automatic gain control to settle
        # Now fix the values
        self.__camera.shutter_speed = self.__camera.exposure_speed
        self.__camera.exposure_mode = 'off'
        g = self.__camera.awb_gains
        self.__camera.awb_mode = 'off'
        self.__camera.awb_gains = g

    def _get_file_name(self):

        format_string = "%Y%m%d_%H%M%S"  # We do not need more precision than seconds.
        target_file_name = datetime.datetime.strftime(datetime.datetime.now(),  format_string) + OUTPUT_EXTENSION
        return Path(self._output_folder) / target_file_name

    def _should_continue(self):

        if self._total_shot_count >= self._photo_count_limit:
            print(f"Maximum photo limit {self._photo_count_limit} has been reached, exiting... ")
            return False

        return True


    def start(self):

        print("Starting...")

        self._set_options()
        self.__last_shot_time = time.time()
        for image in self.__camera.capture_continuous(f"{Path(self._output_folder)}/" + "{timestamp:%Y%m%d_%H%M%S}" + OUTPUT_EXTENSION):
            print(f"Image: {image}\nNumber: {self._total_shot_count}")
            self._total_shot_count += 1
            picam_flash.turn_off()
            time.sleep(self._interval - 2)
            picam_flash.turn_on()
            time.sleep(2)
            if not self._should_continue():
                break

        print("Finished...")

