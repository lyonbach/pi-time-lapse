import argparse
from pathlib import Path
import sys

import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np

EXTENSION = ".png"

MULTIPLE_DIMENSIONS_ERROR_MESSAGE = "Multiple dimensions in the same sequence is not allowed!"


parser = argparse.ArgumentParser(description="Makes timelapse video from the photos in the given folder.")
parser.add_argument("--path", "-P", type=str, required=True)
parser.add_argument("--output_file_name", "-O", type=str, required=True)
parser.add_argument("--dimensions", "-D", type=int, default=0)
parser.add_argument("--frame_per_second", "-FPS", type=int, default=24)
parser.add_argument("--frame_time", "-FT", type=int, default=1)

args = parser.parse_args()


# Get all images.
images_folder = Path(args.path)
if not images_folder.is_dir():
    raise Exception("A valid folder is required.")


dimensions = args.dimensions
width, height = None, None  # While gathering image data we also check if all of the iamges are same size.
                            # But we only do this if dimensions are not given. If dimensions are already given
                            # we scale the images instead.

# Collect all of the image data.
image_data_array = []
for image in sorted(images_folder.glob(f"*{EXTENSION}")):
    frame_data = cv2.imread(str(image))
    if not dimensions:
        height_, width_ = frame_data.shape[:2]
        if width:
            assert width == width_, MULTIPLE_DIMENSIONS_ERROR_MESSAGE
        if height:
            assert height == height_, MULTIPLE_DIMENSIONS_ERROR_MESSAGE
        width = width_
        height = height_

    dimensions = (width, height)
    image_data_array.append(frame_data)

print("Collected image data, writing video...")

# Write video.
video = cv2.VideoWriter(args.output_file_name, cv2.VideoWriter_fourcc(*'MP42'), float(8), dimensions)
for frame_data in image_data_array:
    video.write(frame_data)

video.release()
print(f"Video was successfilly saved as:\n\t{args.output_file_name}")
