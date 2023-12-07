import cv2

VIDEO_FILES = [
    "data/2023-12-01-0159_6-Uranus.AVI",
    "data/2023-11-30-0112_6-Jupiter.AVI",
]
VIDEO_LABELS = ["uranus", "jupiter"]
N_FRAMES = 500
OUTPUT_FPS = 30


codecs = {
    "avi": cv2.VideoWriter_fourcc("M", "J", "P", "G"),
    "mp4": cv2.VideoWriter_fourcc(*"mp4v"),
}


for i, path in enumerate(VIDEO_FILES):
    vid_capture = cv2.VideoCapture(path)

    try:
        # if vid_capture.isOpened():
        print("Error opening the video file")
        fps = vid_capture.get(5)
        print("Frames per second : ", fps, "FPS")
        frame_count = vid_capture.get(7)
        print("Frame count : ", frame_count)
    finally:
        pass

    # Initialize video writer object
    output = cv2.VideoWriter(
        "data/" + VIDEO_LABELS[i] + ".mp4",
        codecs["mp4"],
        OUTPUT_FPS,
        (1000, 800),
    )

    count = 0
    while vid_capture.isOpened() and count < N_FRAMES:
        is_good, frame = vid_capture.read()
        if is_good:
            # crop
            # this should be something configurable
            frame = frame[0:800, 400:1400]
            # comment out if you're not debugging
            cv2.imshow(f"processing test file: {VIDEO_LABELS[i]}", frame)
            # write the frame to the output file
            output.write(frame)
            if cv2.waitKey(20) == ord("q"):
                break
        else:
            break
        count += 1

    vid_capture.release()
    # Release the video capture object
    output.release()


cv2.destroyAllWindows()
