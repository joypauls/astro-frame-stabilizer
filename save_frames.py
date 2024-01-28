import cv2
import numpy as np
from typing import Tuple
from src.cv2_colors import RED, GREEN

FILE = "data/jupiter1.mp4"
OUTPUT_DIR = "data/frames"
FRAME_LABEL = "jupiter"
N_FRAMES = 100
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


count = 0
while vid_capture.isOpened() and count < N_FRAMES:
    is_good, frame = vid_capture.read()
    if is_good:
        cv2.imwrite(f"{OUTPUT_DIR}/{FRAME_LABEL}_{count}.png", frame)

        if cv2.waitKey(20) == ord("q"):
            break

    else:
        break

    count += 1


vid_capture.release()
cv2.destroyAllWindows()
