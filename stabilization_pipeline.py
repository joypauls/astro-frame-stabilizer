import cv2

# VIDEO_FILES = [
#     "data/2023-12-01-0159_6-Uranus.AVI",
#     "data/2023-11-30-0112_6-Jupiter.AVI",
# ]
# VIDEO_LABELS = ["uranus", "jupiter"]

FILE = "data/uranus.mp4"
N_FRAMES = 500
# OUTPUT_FPS = 30

vid_capture = cv2.VideoCapture(FILE)
# only for debugging steps of an algorithm
vid_capture_debug = cv2.VideoCapture(FILE)


codecs = {
    "avi": cv2.VideoWriter_fourcc("M", "J", "P", "G"),
    "mp4": cv2.VideoWriter_fourcc(*"mp4v"),
}

try:
    # if vid_capture.isOpened():
    print("Error opening the video file")
    # Read fps and frame count
    # else:
    # Get frame rate information
    # You can replace 5 with CAP_PROP_FPS as well, they are enumerations
    fps = vid_capture.get(5)
    print("Frames per second : ", fps, "FPS")

    # Get frame count
    # You can replace 7 with CAP_PROP_FRAME_COUNT as well, they are enumerations
    frame_count = vid_capture.get(7)
    print("Frame count : ", frame_count)
finally:
    pass


# # Initialize video writer object
# output = cv2.VideoWriter(
#     VIDEO_LABELS[0] + ".mp4",
#     codecs["mp4"],
#     OUTPUT_FPS,
#     (1000, 800),
# )

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
        radius = 150
        cropped_frame = frame[
            centroid[1] - radius : centroid[1] + radius,
            centroid[0] - radius : centroid[0] + radius,
        ]

        print(frame.shape)

        cv2.rectangle(
            cropped_frame,
            (centroid[0] - 2, centroid[1] - 2),
            (centroid[0] + 2, centroid[1] + 2),
            (0, 0, 255),
            -1,
        )

        # put text and highlight the center
        cv2.imshow("frame", cropped_frame)

        if cv2.waitKey(20) == ord("q"):
            break

    else:
        break

    count += 1


# Release the video capture object
vid_capture.release()
cv2.destroyAllWindows()
