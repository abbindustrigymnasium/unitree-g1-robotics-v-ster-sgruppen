import os
import time
import threading

import cv2
from dotenv import load_dotenv
from pathlib import Path

# Load the project's .env file by searching this folder and its parents.
for parent in Path(__file__).resolve().parents:
    env_file = parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        break

from .board_detection import BoardDetector
from .perspective import BoardPerspective
from .piece_recognition import PieceRecognizer


UNITREE_G1_IP = os.getenv("UNITREE_G1_IP")

DEFAULT_CAMERA_SOURCE = os.getenv("CAMERA_SOURCE")
if not DEFAULT_CAMERA_SOURCE:
    DEFAULT_CAMERA_SOURCE = (
        f"rtsp://{UNITREE_G1_IP}:8554/cam"
        if UNITREE_G1_IP else "0"
    )

BOARD_SIZE = 600


class TicTacToeCamera:
    def __init__(self, camera_source=DEFAULT_CAMERA_SOURCE, show_window=True):
        if isinstance(camera_source, str) and camera_source.isdigit():
            camera_source = int(camera_source)

        backend = (
            cv2.CAP_FFMPEG if isinstance(camera_source, str)
            else cv2.CAP_V4L2
        )

        self.cap = cv2.VideoCapture(camera_source, backend)

        if not self.cap.isOpened():
            raise RuntimeError(f"Could not open camera: {camera_source}")

        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.detector = BoardDetector()
        self.perspective = BoardPerspective(BOARD_SIZE)
        self.pieces = PieceRecognizer(BOARD_SIZE)

        self.show_window = show_window
        self.latest_frame = None
        self.capture_lock = threading.Lock()
        self.capture_stop = threading.Event()

        self.capture_thread = threading.Thread(
            target=self._capture_latest_frame,
            daemon=True
        )
        self.capture_thread.start()

        print(f"Tic-tac-toe camera initialized: {camera_source}")

    def _capture_latest_frame(self):
        while not self.capture_stop.is_set():
            success, frame = self.cap.read()

            if not success or frame is None:
                time.sleep(0.01)
                continue

            with self.capture_lock:
                self.latest_frame = frame

    def read_latest_frame(self):
        with self.capture_lock:
            if self.latest_frame is None:
                return False, None
            return True, self.latest_frame.copy()

    def analyze_frame(self, frame):
        """
        Analyze one frame.

        Returns a dictionary. If the board isn't fully detected,
        board_state is None.
        """
        corners, marker_ids = self.detector.detect(frame)

        if corners is None:
            return {
                "board_detected": False,
                "marker_ids": marker_ids,
                "board_state": None,
                "warped_image": None,
            }

        warped, _ = self.perspective.warp(frame, corners)
        board_state = self.pieces.recognize(warped)

        return {
            "board_detected": True,
            "marker_ids": marker_ids,
            "board_state": board_state,
            "warped_image": warped,
        }

    def run(self):
        print("Camera running. Press Q in the preview window to quit.")

        try:
            while True:
                success, frame = self.read_latest_frame()

                if not success:
                    time.sleep(0.01)
                    continue

                result = self.analyze_frame(frame)

                if result["board_detected"]:
                    display = frame.copy()
                    self.detector.draw_corners(display, self.detector.detect(frame)[0])

                    warped_display = result["warped_image"].copy()
                    self.pieces.draw_board_state(
                        warped_display, result["board_state"]
                    )

                    print("\rBoard:", result["board_state"], end="")

                    if self.show_window:
                        cv2.imshow("G1 Camera - Board", display)
                        cv2.imshow("Top-down board", warped_display)
                else:
                    display = frame.copy()
                    cv2.putText(
                        display, "Board not detected - show all 4 markers",
                        (15, 35), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255), 2
                    )
                    if self.show_window:
                        cv2.imshow("G1 Camera - Board", display)

                if self.show_window and (cv2.waitKey(1) & 0xFF == ord("q")):
                    break

        finally:
            self.close()

    def close(self):
        self.capture_stop.set()
        self.cap.release()

        if self.capture_thread.is_alive():
            self.capture_thread.join(timeout=1)

        cv2.destroyAllWindows()
        print("\nCamera closed.")


if __name__ == "__main__":
    camera = None
    try:
        camera = TicTacToeCamera()
        camera.run()
    except KeyboardInterrupt:
        pass
    finally:
        if camera is not None:
            camera.close()
