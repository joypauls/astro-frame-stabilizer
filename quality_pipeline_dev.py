import cv2
import numpy as np
import argparse

# from stabilization_pipeline_dev as sp
from player import Player
from src.cv2_colors import RED, GREEN

# FILE = "data/uranus.mp4"
FILE = "data/jupiter1_downsampled.mp4"
# FILE = "data/jupiter2_downsampled.mp4"
# FILE = "data/jupiter2.mp4"
N_FRAMES = 500
CROP_HALF_SIDE = 300
MARKER_HALF_SIDE = 5


# # initialize video capture objects
# vid_capture = cv2.VideoCapture(FILE)
# fps = vid_capture.get(5)
# print(f"Frame Rate: {fps} FPS")
# frame_count = vid_capture.get(7)
# print(f"Frame Count : {frame_count}")


def _parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "test", type=str, default="", required=False, help="Replace this"
    # )
    args = parser.parse_args()
    return args


def imshow_named(img: np.ndarray, name: str, x: int = 0, y: int = 0):
    # create a window and move
    cv2.namedWindow(name)
    cv2.moveWindow(name, x, y)
    cv2.imshow(name, img)


def _quality_filter(frame: cv2.UMat) -> cv2.UMat:
    # convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # apply gaussian blur
    # gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # print(np.max(gray))
    edges = cv2.Laplacian(gray, -1, ksize=5)
    # edges = cv2.Sobel(src=gray, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
    # edges = cv2.Canny(gray, 40, 140)
    # edges = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return edges


def _raw_filter(frame: cv2.UMat) -> cv2.UMat:
    # convert to grayscale
    # new = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
    return frame


if __name__ == "__main__":
    args = _parse()
    p = Player(file=FILE, filter=_raw_filter, filter_debug=_quality_filter)
    p.play()
