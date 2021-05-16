import datetime
import math
from pathlib import Path
import time

from picamera.array import PiRGBArray
from picamera import PiCamera

import picam_flash

OUTPUT_EXTENSION = ".png"

# TODO: ADD "DO UNTIL" FUNCTIONALITY
# TODO: ADD LOGGING

class TimeLapseWorker:

    def __init__(self, interval: int, output_folder: str, photo_count_limit: int=0, flash_warmup_time:float=0):

        """
        :interval         : Time (seconds) to wait until next shot.
        :output_folder    : Folder to save the shots to.
        :phoho_count_limit: Stops after this value has been reached.
        :flash_warmup_time: Sets the value to wait for to turn on the flash before shooting a photo.
        """

        photo_count_limit = math.inf if photo_count_limit <= 0 else int(photo_count_limit)

        if flash_warmup_time < 0:
            raise ValueError(f"Minimum flash warm-up time must be a positive value.")

        self._flash_warmup_time = flash_warmup_time
        self._interval = interval

        if interval <= self._flash_warmup_time:
            raise ValueError(
                f"Minimum interval must be less then flash warm-up time: {self._flash_warmup_time} !< {self._interval}")


        # Check if output folder exists.
        self._output_folder = Path(output_folder)
        if not self._output_folder.is_dir():
            raise IOError("Given target folder does not exist!")

        self._photo_count_limit = photo_count_limit or float("inf")

        # We initialize total shoot count to the number of photos in the given output folder.
        self._total_shot_count = len(list(self._output_folder.glob(f"*{OUTPUT_EXTENSION}")))
        self.__camera = PiCamera()

    def _get_file_name(self):

        format_string = "%Y%m%d_%H%M%S"  # We do not need more precision than seconds.
        target_file_name = datetime.datetime.strftime(datetime.datetime.now(),  format_string) + OUTPUT_EXTENSION
        return Path(self._output_folder) / target_file_name

    def _get_overall_info(self):

        information_message = "Starting with the following options:\n"
        information_message += f"\tInterval: {self._interval} seconds.\n"

        if self._flash_warmup_time:
            information_message += "\tFlash is requested, picam-flash msut be powered and connected to the wi-fi.\n"
            information_message += f"\tFlash Warm-Up Time: {self._flash_warmup_time} seconds.\n"

        information_message += f"\tOutput Folder: {self._output_folder}\n"

        if self._photo_count_limit != math.inf:
            information_message += f"\tPhoto Count Limit: {self._photo_count_limit}\n"
            information_message += "\t* Will stop after this limit  has been reached.\n"
        else:
            information_message += "\tNo count limit has been provided.\n"

        return information_message

    def _should_continue(self):

        if self._total_shot_count >= self._photo_count_limit:
            print(f"Maximum photo limit {self._photo_count_limit} has been reached, exiting... ")
            return False

        return True

    def _set_flash(self, state):

        """
        Handles flash.
        """

        # We must wrap everything in a try except block to not interrupt the camera if something about the flash goes
        # wrong.

        if not self._flash_warmup_time:
            return

        try:
            if state == "on":
                print("[d]: Turning flash on.")
                picam_flash.turn_on()

            elif state == "off":
                print("[d]: Turning flash off.")
                picam_flash.turn_off()

            elif state == "stop":
                print("[d]: Stopping picam_flash...")
                picam_flash.stop_server()

        except Exception as error:
            print(f"Unable to connect to wireless flash, Original Error\n\t{error}")

    def _set_options(self):

        self.__camera.resolution = (1024, 1024)

    def start(self):

        # Print some information about the process.
        print(self._get_overall_info())

        self._set_options()

        # Prepare for the first shot. Turn on the flash, and give the camera some time to get ready.
        self._set_flash("on")
        time.sleep(self._flash_warmup_time)

        for image in self.__camera.capture_continuous(f"{Path(self._output_folder)}/" + "{timestamp:%Y%m%d_%H%M%S}" + OUTPUT_EXTENSION):

            # After shooting turn off the flash if we are using flash.
            # Function itself handles if flash is requested or not.
            self._set_flash("off")
            print(f"Image: {image}\nNumber: {self._total_shot_count}")
            self._total_shot_count += 1

            # Wait for the next shot time.
            time.sleep(self._interval - self._flash_warmup_time) 

            # Prepare for the next shot. Turn on the flash, and give the camera some time to get ready.
            self._set_flash("on")
            time.sleep(self._flash_warmup_time)
            if not self._should_continue():
                break

        print(f"Finished. Photos were saved under\n\t{self._output_folder}")
        self._set_flash("stop")
