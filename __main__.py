#!./interpreter/bin/python
import datetime
from pathlib import Path
import time

import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

OUTPUT_EXTENSION = ".png"

class TimeLapseWorker:

    def __init__(self, interval: int, output_folder: str, photo_count_limit: int=None):  # TODO: ADD "DO UNTIL" FUNCTIONALITY

        """
        :interval     : Time (seconds) to wait until next shot.
        :output_folder: Folder to save the shots to.
        """

        self._interval = interval

        # Check if output folder exists.
        self._output_folder = Path(output_folder)
        if not self._output_folder.is_dir():
            raise IOError("Given target folder does not exist!")

        self._should_continue = True
        self._photo_count_limit = photo_count_limit or float("inf")

        self._total_shot_count = 0
        self.__last_shot_time = None
        self.__camera = None

    def _warm_up(self):

        self.__camera = PiCamera()
        self.__camera.resolution = (800, 800)

    def _get_file_name(self):

        format_string = "%Y%m%d_%H%M%S"  # We do not need more precision than seconds.
        target_file_name = datetime.datetime.strftime(datetime.datetime.now(),  format_string) + OUTPUT_EXTENSION
        return Path(self._output_folder) / target_file_name

    def _shoot(self):

        if time.time() - self.__last_shot_time <= self._interval:
            return

        print("Shooting!")

        time.sleep(1)
        target_file = self._get_file_name()
        self._total_shot_count += 1#
        self.__last_shot_time = time.time()

        raw_capture = PiRGBArray(self.__camera)

        self.__camera.capture(raw_capture, format="bgr")
        image = raw_capture.array

        cv2.imwrite(str(target_file), image)

        print(f"Successfully saved file as:\n\t{target_file}.")
        print(f"Total shots: {self._total_shot_count}")

    def _do_checks(self):

        if self._total_shot_count >= self._photo_count_limit:
            print(f"Maximum photo limit {self._photo_count_limit} has been reached, exiting... ")
            self._should_continue = False

    def start(self):

        print("Starting...")
        self._warm_up()
        self.__last_shot_time = time.time()

        # Main loop.
        while True:

            # Check every 0.1 seconds.
            time.sleep(.1)

            self._shoot()

            self._do_checks()
            if not self._should_continue:
                break

        print("Finished...")



if __name__ == "__main__":

    target_folder = Path(__file__).parent / "test_photos"
    time_lapse_worker = TimeLapseWorker(5 * 60, target_folder, 500)
    time_lapse_worker.start()
