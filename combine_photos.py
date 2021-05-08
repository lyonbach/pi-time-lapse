import argparse
from pathlib import Path
import sys

import cv2
from cv2 import VideoWriter, VideoWriter_fourcc
import numpy as np

parser = argparse.ArgumentParser(description="Makes timelapse video from the photos in the given folder.")
parser.add_argument("--path", "-P", type=str)
parser.add_argument("--width", "-W", type=int, default=800)
parser.add_argument("--height", "-H", type=int, default=800)
parser.add_argument("--frame_per_second", "-FPS", type=int, default=24)
parser.add_argument("--frame_time", "-FT", type=int, default=1)


args = parser.parse_args()

# Get all images.
images_folder = Path(args.path)
if not images_folder.is_dir():
    raise Exception("A valid folder is required.")

all_images = images_folder.glob("*.png")

# Start video buffer.
fourcc = VideoWriter_fourcc(*'MP42')
video = VideoWriter('./output.avi', fourcc, float(8), (args.width, args.height))

for image in sorted(all_images):

    # Read image data.
    frame_data = cv2.imread(str(image), cv2.IMREAD_UNCHANGED)
    video.write(frame_data)

video.release()