"""
Render a video file with opencvsince there is no built-in
video player for my AVI's on a mac

Can be run standalone, or imported
"""
import cv2
import numpy as np
import argparse
from typing import Optional, Callable

TEST_VIDEO_FILE = "data/jupiter1.mp4"
N_FRAMES = 500


def _parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", type=str, default=None, required=False, help="Path to video file"
    )
    parser.add_argument(
        "--dir",
        type=str,
        default=None,
        required=False,
        help="Directory to display choices from",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=None,
        required=False,
        help="Only first n frames",
    )
    args = parser.parse_args()
    return args


# try:
#     vid_capture = cv2.VideoCapture(args.video_file)
#     print("Error opening the video file")
#     fps = vid_capture.get(5)
#     print(fps, "FPS")
#     frame_count = vid_capture.get(7)
#     print("Frames: ", frame_count)
# except Exception as e:
#     print(e)


# count = 0
# while vid_capture.isOpened() and count < N_FRAMES:
#     # vid_capture.read() methods returns a tuple, first element is a bool
#     # and the second is frame
#     is_good, frame = vid_capture.read()
#     if is_good:
#         # # crop
#         # frame = frame[0:900, 400:]

#         cv2.imshow("Frame", frame)
#         # 20 is in milliseconds, try to increase the value, say 50 and observe
#         key = cv2.waitKey(20)

#         if key == ord("q"):
#             break
#     else:
#         break

#     count += 1


class Player:
    """
    Plays a video file

    """

    def __init__(
        self,
        file: Optional[str] = None,
        dir: Optional[str] = None,
        filter: Optional[Callable] = None,
        n: float = np.inf,
    ):
        # from args
        self.file = file
        self.dir = dir
        self.n = n
        self.filter = filter

        # derived
        self.capture = None
        self.fps = None
        if file:
            self.capture = cv2.VideoCapture(file)
            self.fps = self.capture.get(5)

    def play(self):
        """actual render loop"""
        if not self.file:
            raise Exception("No file selected or passed in as an arg")
        title = f"Playing {self.file}" if self.file else "player.py"
        count = 0
        while self.capture.isOpened() and count < self.n:
            is_good, frame = self.capture.read()
            if is_good:
                self.filter(frame) if self.filter else None
                cv2.imshow(title, frame)
                key = cv2.waitKey(20)
                if key == ord("q"):
                    break
            else:
                break
            count += 1
        self.close()

    def close(self):
        """close the video file"""
        self.capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    args = _parse()
    p = Player(file=args.file, dir=args.dir, n=args.n)
    p.play()


# # Release the video capture object
# vid_capture.release()
# cv2.destroyAllWindows()
