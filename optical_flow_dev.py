import cv2
import numpy as np
import argparse

# from stabilization_pipeline_dev as sp
from player import Player
from src.cv2_colors import RED, GREEN

# FILE = "data/uranus.mp4"
# FILE = "data/uranus_downsampled.mp4"
FILE = "data/jupiter1.mp4"
# FILE = "data/jupiter1_downsampled.mp4"
# FILE = "data/jupiter2.mp4"
# FILE = "data/jupiter2_downsampled.mp4"
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
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)[:, :, 0]

    # apply blur to minimize affect of noise on gradients
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    # gray = cv2.medianBlur(gray, 3)
    # print(np.max(gray))

    # simple Laplacian version (for score should take variance)
    # too noisy!
    # edges = cv2.Laplacian(gray, -1, ksize=7)

    # gradient magnitude verison
    grad_x = cv2.Sobel(
        gray,
        cv2.CV_16S,
        1,
        0,
        ksize=-1,
        scale=1,
        delta=0,
        borderType=cv2.BORDER_DEFAULT,
    )
    grad_y = cv2.Sobel(
        gray,
        cv2.CV_16S,
        0,
        1,
        ksize=-1,
        scale=1,
        delta=0,
        borderType=cv2.BORDER_DEFAULT,
    )
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    edges = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    # edges = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    score = edges.var()

    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    edges = cv2.resize(edges, (int(edges.shape[1] / 2), int(edges.shape[0] / 2)))

    # annotate
    cv2.putText(
        edges,
        f"Quality Score: {score}",
        (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        GREEN,
        1,
        cv2.LINE_AA,
    )

    return edges


def _raw_filter(frame: cv2.UMat) -> cv2.UMat:
    # convert to grayscale
    frame = cv2.resize(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2)))
    return frame


if __name__ == "__main__":
    args = _parse()
    p = Player(file=FILE, filter=_raw_filter, filter_debug=_quality_filter)
    p.play()
