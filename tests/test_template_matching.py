#!../interpreter/bin/python
from pathlib import Path
import sys
sys.path.append("/home/lyonbach/Repositories/pi-time-lapse")

import cv2
import camera_alignment as ca


if __name__ == "__main__":

    search_images = list(Path("/home/lyonbach/Pictures").glob("*search*.png"))

    source_image_path = str(search_images[0])
    source_image_path = "/home/lyonbach/Pictures/search_image_2_not_aligned.png"

    should_continue = True
    while should_continue:
        for image in search_images:
            print(f"Image\n\t:{str(image)}")
            assertions, showcase_matrix = ca.get_alignment_info(str(image))
            cv2.imshow("temp", showcase_matrix)
            if cv2.waitKey(0) == ord('q'):
                should_continue = False
                break
    cv2.destroyAllWindows()
