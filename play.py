"""Render a video file with opencv"""
import cv2
import argparse

VIDEO_FILE = "data/2023-12-01-0159_6-Uranus.AVI"
N_FRAMES = 1000

parser = argparse.ArgumentParser()
parser.add_argument(
    "video_file", type=str, default=VIDEO_FILE, help="Path to video file"
)
args = parser.parse_args()

# Create a video capture object, in this case we are reading the video from a file
vid_capture = cv2.VideoCapture(args.video_file)

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


count = 0
while vid_capture.isOpened() and count < N_FRAMES:
    # vid_capture.read() methods returns a tuple, first element is a bool
    # and the second is frame
    is_good, frame = vid_capture.read()
    if is_good:
        # crop
        frame = frame[0:900, 400:]

        cv2.imshow("Frame", frame)
        # 20 is in milliseconds, try to increase the value, say 50 and observe
        key = cv2.waitKey(20)

        if key == ord("q"):
            break
    else:
        break

    count += 1


# Release the video capture object
vid_capture.release()
cv2.destroyAllWindows()
