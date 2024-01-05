import cv2
import numpy as np
from typing import Tuple
from src.cv2_colors import RED, GREEN

# VIDEO_FILES = [
#     "data/2023-12-01-0159_6-Uranus.AVI",
#     "data/2023-11-30-0112_6-Jupiter.AVI",
# ]
# VIDEO_LABELS = ["uranus", "jupiter"]

# FILE = "data/uranus.mp4"
VIDEO = "jupiter1.mp4"
FILE = "data/" + VIDEO
# FILE = "data/jupiter2.mp4"
N_FRAMES = 500
CROP_HALF_SIDE = 300
MARKER_HALF_SIDE = 5
CODECS = {
    "avi": cv2.VideoWriter_fourcc("M", "J", "P", "G"),
    "mp4": cv2.VideoWriter_fourcc(*"mp4v"),
}

# initialize video capture objects
vid_capture = cv2.VideoCapture(FILE)
fps = vid_capture.get(5)
print(f"Frame Rate: {fps} FPS")
frame_count = vid_capture.get(7)
print(f"Frame Count : {frame_count}")


def imshow_named(img: np.ndarray, name: str, x: int = 0, y: int = 0):
    # create a window and move
    cv2.namedWindow(name)
    cv2.moveWindow(name, x, y)
    cv2.imshow(name, img)


def build_algorithm_visual(
    binary_frame: np.ndarray,
    centroid: tuple[int, int],
    r1: int = MARKER_HALF_SIDE,
    r2: int = CROP_HALF_SIDE,
) -> cv2.UMat:
    visual = cv2.cvtColor(binary_frame, cv2.COLOR_GRAY2BGR)
    # draw the marker for centroid
    cv2.rectangle(
        visual,
        (centroid[0] - r1, centroid[1] - r1),
        (centroid[0] + r1, centroid[1] + r1),
        RED,
        -1,
    )
    # draw the cropped padded boundary around object
    cv2.rectangle(
        visual,
        (centroid[0] - r2, centroid[1] - r2),
        (centroid[0] + r2, centroid[1] + r2),
        RED,
        2,
    )
    # resize to fit on laptop screen
    return cv2.resize(visual, (int(visual.shape[1] / 2), int(visual.shape[0] / 2)))


def adjust_output_frame(
    frame: np.ndarray, centroid: Tuple[int, int], r: int = CROP_HALF_SIDE
) -> cv2.UMat:
    # corners of the cropping square, they can be negative which is handled below
    crop_y0 = centroid[1] - r
    crop_y1 = centroid[1] + r
    crop_x0 = centroid[0] - r
    crop_x1 = centroid[0] + r

    # handle padding from crop that goes out of bounds
    if any(
        [
            crop_y0 < 0,
            crop_y1 > frame.shape[0],
            crop_x0 < 0,
            crop_x1 > frame.shape[1],
        ]
    ):
        # padding for image if any crop is out of bounds
        top_pad = 0
        bottom_pad = 0
        left_pad = 0
        right_pad = 0
        if crop_y0 < 0:
            top_pad = abs(crop_y0)
            crop_y0 = 0
        if crop_y1 > frame.shape[0]:
            bottom_pad = crop_y1 - frame.shape[0]
            crop_y1 = frame.shape[0]
        if crop_x0 < 0:
            left_pad = abs(crop_x0)
            crop_x0 = 0
        if crop_x1 > frame.shape[1]:
            right_pad = crop_x1 - frame.shape[1]
            crop_x1 = frame.shape[1]

        cropped_frame = frame[crop_y0:crop_y1, crop_x0:crop_x1]
        cropped_frame = cv2.copyMakeBorder(
            cropped_frame,
            top_pad,
            bottom_pad,
            left_pad,
            right_pad,
            cv2.BORDER_CONSTANT,
            value=GREEN,
        )
    else:
        cropped_frame = frame[crop_y0:crop_y1, crop_x0:crop_x1]

    return cropped_frame


stable_frame_list = []
count = 0
while vid_capture.isOpened() and count < N_FRAMES:
    # print(count)

    # vid_capture.read() methods returns a tuple, first element is a bool
    # and the second is frame
    is_good, frame = vid_capture.read()
    if is_good:
        # STABILIZATION ALGO

        # crop
        # this should be something configurable
        # frame = frame[0:800, 400:1400]

        # convert LAB and pick luminance channel
        luminance = cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)[:, :, 0]

        # fast blur - goal is to get rid of high frequency noise
        luminance = cv2.GaussianBlur(luminance, (5, 5), 0)

        # binarize luminance to get object mask
        _, luminance = cv2.threshold(
            luminance, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        # calculate moments of binary image
        M = cv2.moments(luminance)

        # calculate x,y coordinate of center
        centroid = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # crop and expand frame where needed
        cropped_frame = adjust_output_frame(frame, centroid)

        stable_frame_list.append(cropped_frame)

    else:
        break

    count += 1


# Release the video capture object
vid_capture.release()


# wrap up calculations
stack = np.stack(stable_frame_list)
print(stack.shape)
print(stack[0].dtype)
mean_image = np.mean(stack, axis=0).astype(dtype="uint8")
print(mean_image.shape)
cv2.imshow("Mean Image", mean_image)
cv2.waitKey(-1)  # wait until any key is pressed
cv2.imwrite(f"data/{VIDEO}_stacked_simple.png", mean_image)
