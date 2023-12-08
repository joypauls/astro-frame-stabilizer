import cv2
import numpy as np

# VIDEO_FILES = [
#     "data/2023-12-01-0159_6-Uranus.AVI",
#     "data/2023-11-30-0112_6-Jupiter.AVI",
# ]
# VIDEO_LABELS = ["uranus", "jupiter"]

# FILE = "data/uranus.mp4"
FILE = "data/jupiter.mp4"
N_FRAMES = 500
# only for debugging steps of an algorithm
DEBUG = True
CODECS = {
    "avi": cv2.VideoWriter_fourcc("M", "J", "P", "G"),
    "mp4": cv2.VideoWriter_fourcc(*"mp4v"),
}

# initialize video capture objects
vid_capture = cv2.VideoCapture(FILE)
if DEBUG:
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
    r1: int = 4,
    r2: int = 100,
):
    visual = cv2.cvtColor(binary_frame, cv2.COLOR_GRAY2BGR)
    # draw the marker for centroid
    cv2.rectangle(
        visual,
        (centroid[0] - r1, centroid[1] - r1),
        (centroid[0] + r1, centroid[1] + r1),
        (0, 255, 0),
        -1,
    )
    # draw the cropped padded boundary around object
    cv2.rectangle(
        visual,
        (centroid[0] - r2, centroid[1] - r2),
        (centroid[0] + r2, centroid[1] + r2),
        (0, 255, 0),
        2,
    )
    # resize to fit on laptop screen
    return cv2.resize(visual, (int(visual.shape[1] / 2), int(visual.shape[0] / 2)))


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
        pad = 300
        cropped_frame = frame[
            centroid[1] - pad : centroid[1] + pad,
            centroid[0] - pad : centroid[0] + pad,
        ]

        # if DEBUG:
        # print(frame.shape)

        # put text and highlight the center
        cv2.imshow("Generated Output", cropped_frame)
        # put anything here to visualize while processing
        # for instance the binary thresholded image
        imshow_named(
            build_algorithm_visual(luminance, centroid, 4, pad),
            "Algorithm",
            x=cropped_frame.shape[1],
            y=0,
        )

        if cv2.waitKey(20) == ord("q"):
            break

    else:
        break

    count += 1


# Release the video capture object
vid_capture.release()
cv2.destroyAllWindows()
