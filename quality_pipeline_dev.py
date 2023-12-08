import cv2
import numpy as np
import argparse
import stabilization_pipeline_dev as sp
from src.cv2_colors import RED, GREEN

# FILE = "data/uranus.mp4"
FILE = "data/jupiter1.mp4"
# FILE = "data/jupiter2.mp4"
N_FRAMES = 500
CROP_HALF_SIDE = 300
MARKER_HALF_SIDE = 5


# initialize video capture objects
vid_capture = cv2.VideoCapture(FILE)
fps = vid_capture.get(5)
print(f"Frame Rate: {fps} FPS")
frame_count = vid_capture.get(7)
print(f"Frame Count : {frame_count}")


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("test", type=str, default="", help="Replace this")
    args = parser.parse_args()
    return args


def main():
    # parse command line arguments
    args = parse()

    # logic


if __name__ == "__main__":
    main()
