"""Goal is to generate some small/short files from longer real data."""
import cv2

VIDEO_FILES = [
    "data/2023-12-01-0159_6-Uranus.AVI",
    "data/2023-11-30-0112_6-Jupiter.AVI",
    "data/2023-12-08-0151_9-Jupiter.AVI",
]
VIDEO_LABELS = ["uranus", "jupiter1", "jupiter2"]
OFFSETS = [0, 0, 0]
N_FRAMES = 500
OUTPUT_FPS = 30
CODECS = {
    "avi": cv2.VideoWriter_fourcc("M", "J", "P", "G"),
    "mp4": cv2.VideoWriter_fourcc(*"mp4v"),
}

for i, path in enumerate(VIDEO_FILES):
    try:
        vid_capture = cv2.VideoCapture(path)
        fps = vid_capture.get(5)
        print("Frames per second : ", fps, "FPS")
        frame_count = vid_capture.get(7)
        print("Frame count : ", frame_count)
    except Exception as e:
        print(f"Error reading {path}")
        print(e)

    # Initialize video writer object
    output = cv2.VideoWriter(
        "data/" + VIDEO_LABELS[i] + ".mp4",
        CODECS["mp4"],
        OUTPUT_FPS,
        (1000, 800),
    )

    count = 0
    while vid_capture.isOpened() and count < N_FRAMES:
        is_good, frame = vid_capture.read()
        if is_good:
            # crop
            # this should be something configurable
            frame = frame[
                OFFSETS[i] : 800 + OFFSETS[i], 400 + OFFSETS[i] : 1400 + OFFSETS[i]
            ]
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
