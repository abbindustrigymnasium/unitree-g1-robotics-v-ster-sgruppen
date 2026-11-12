# ============================================================
# ROCK PAPER SCISSORS - CAMERA RECOGNITION
# Unitree G1 Camera Integration
#
# How it works:
# 1. Opens the G1 camera
# 2. Detects the player's hand
# 3. Recognizes rock, paper or scissors
# 4. Takes 10 samples
# 5. Uses majority voting to determine the result
# 6. Returns the result to the main game
# 7. Returns "UNKNOWN" if it can't confidently recognize
# ============================================================

import cv2
import mediapipe as mp
import os
import urllib.request
import math
import time

from pathlib import Path
from collections import Counter


# ============================================================
# SETTINGS
# ============================================================

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "hand_landmarker.task"
)

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/"
    "hand_landmarker.task"
)

# Unitree G1 camera
CAMERA_SOURCE = os.getenv("CAMERA_SOURCE", "/dev/video2")

NUMBER_OF_FRAMES = 10
MINIMUM_VOTES = 6
SAMPLE_INTERVAL = 0.06


# ============================================================
# DOWNLOAD MODEL IF NEEDED
# ============================================================

def download_model():

    if not os.path.exists(MODEL_PATH):

        print("Downloading MediaPipe hand model...")

        urllib.request.urlretrieve(
            MODEL_URL,
            MODEL_PATH
        )

        print("Model downloaded!")


# ============================================================
# ANGLE CALCULATION
# ============================================================

def angle_3d(a, b, c):

    ba = [
        a.x - b.x,
        a.y - b.y,
        a.z - b.z
    ]

    bc = [
        c.x - b.x,
        c.y - b.y,
        c.z - b.z
    ]

    dot = sum(
        ba[i] * bc[i] for i in range(3)
    )

    mag_ba = math.sqrt(
        sum(v * v for v in ba)
    )

    mag_bc = math.sqrt(
        sum(v * v for v in bc)
    )

    if mag_ba == 0 or mag_bc == 0:
        return 0

    cosine = dot / (mag_ba * mag_bc)

    cosine = max(-1, min(1, cosine))

    return math.degrees(
        math.acos(cosine)
    )


# ============================================================
# FINGER DETECTION
# ============================================================

def finger_angles(landmarks, mcp, pip, dip, tip):

    pip_angle = angle_3d(
        landmarks[mcp],
        landmarks[pip],
        landmarks[dip]
    )

    dip_angle = angle_3d(
        landmarks[pip],
        landmarks[dip],
        landmarks[tip]
    )

    return pip_angle, dip_angle


def finger_is_extended(landmarks, mcp, pip, dip, tip):

    pip_angle, dip_angle = finger_angles(
        landmarks, mcp, pip, dip, tip
    )

    return (
        pip_angle > 120
        and dip_angle > 130
    )


# ============================================================
# GESTURE RECOGNITION
# ============================================================

def recognize_gesture(landmarks):

    index = finger_is_extended(
        landmarks, 5, 6, 7, 8
    )

    middle = finger_is_extended(
        landmarks, 9, 10, 11, 12
    )

    ring = finger_is_extended(
        landmarks, 13, 14, 15, 16
    )

    pinky = finger_is_extended(
        landmarks, 17, 18, 19, 20
    )

    extended_count = sum([
        index,
        middle,
        ring,
        pinky
    ])

    # SCISSORS
    if index and middle and not pinky:
        return "SCISSORS"

    # PAPER
    elif extended_count == 4:
        return "PAPER"

    # ROCK
    elif extended_count == 0:
        return "ROCK"

    return "UNKNOWN"


# ============================================================
# HAND DRAWING
# ============================================================

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]


def draw_hand(frame, landmarks):

    height, width, _ = frame.shape

    for start_idx, end_idx in HAND_CONNECTIONS:

        p1 = landmarks[start_idx]
        p2 = landmarks[end_idx]

        x1 = int(p1.x * width)
        y1 = int(p1.y * height)

        x2 = int(p2.x * width)
        y2 = int(p2.y * height)

        cv2.line(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

    for point in landmarks:

        x = int(point.x * width)
        y = int(point.y * height)

        cv2.circle(
            frame,
            (x, y),
            4,
            (0, 0, 255),
            -1
        )


# ============================================================
# CAMERA RECOGNIZER CLASS
# ============================================================

class CameraRecognizer:

    def __init__(self, camera_source=CAMERA_SOURCE):

        download_model()

        # Initialize MediaPipe
        BaseOptions = mp.tasks.BaseOptions

        HandLandmarker = mp.tasks.vision.HandLandmarker

        HandLandmarkerOptions = (
            mp.tasks.vision.HandLandmarkerOptions
        )

        RunningMode = mp.tasks.vision.RunningMode

        options = HandLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_buffer=Path(MODEL_PATH).read_bytes()
            ),
            running_mode=RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.landmarker = (
            HandLandmarker.create_from_options(options)
        )

        # Convert numeric camera strings to integers
        if isinstance(camera_source, str) and camera_source.isdigit():
            camera_source = int(camera_source)

        # ----------------------------------------------------
        # OPEN CAMERA
        # ----------------------------------------------------

        if os.name == "nt":

            # Windows
            self.cap = cv2.VideoCapture(
                camera_source,
                cv2.CAP_DSHOW
            )

        else:

            # Linux / Unitree G1
            self.cap = cv2.VideoCapture(
                camera_source,
                cv2.CAP_V4L2
            )

        if not self.cap.isOpened():

            self.landmarker.close()

            raise RuntimeError(
                f"Could not open camera: {camera_source}"
            )

        self.last_timestamp_ms = -1

        print("Camera recognizer initialized!")
        print(f"Using camera: {camera_source}")


    # ========================================================
    # CAPTURE AND RECOGNIZE ONE FRAME
    # ========================================================

    def process_frame(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp_ms = int(
            time.monotonic() * 1000
        )

        timestamp_ms = max(
            timestamp_ms,
            self.last_timestamp_ms + 1
        )

        self.last_timestamp_ms = timestamp_ms

        result = self.landmarker.detect_for_video(
            mp_image,
            timestamp_ms
        )

        if not result.hand_landmarks:
            return "UNKNOWN", frame

        landmarks_2d = result.hand_landmarks[0]

        landmarks_3d = result.hand_world_landmarks[0]

        gesture = recognize_gesture(landmarks_3d)

        draw_hand(frame, landmarks_2d)

        return gesture, frame


    # ========================================================
    # DETECT PLAYER MOVE
    # ========================================================

    def detect_player_move(self):

        print("\nWaiting for player's gesture...")

        votes = []

        samples_taken = 0

        last_sample_time = 0

        while samples_taken < NUMBER_OF_FRAMES:

            success, frame = self.cap.read()

            if not success or frame is None:

                print("Could not read camera frame.")

                break

            # Mirror camera image
            frame = cv2.flip(frame, 1)

            current_time = time.monotonic()

            gesture, display_frame = self.process_frame(
                frame
            )

            # Take samples at fixed intervals
            if (
                current_time - last_sample_time
                >= SAMPLE_INTERVAL
            ):

                votes.append(gesture)

                samples_taken += 1

                last_sample_time = current_time

                print(
                    f"Frame {samples_taken}: {gesture}"
                )

            # Display camera
            cv2.putText(
                display_frame,
                f"Recognized: {gesture}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                display_frame,
                f"Frames: {samples_taken}/{NUMBER_OF_FRAMES}",
                (10, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2
            )

            cv2.imshow(
                "Rock Paper Scissors Camera",
                display_frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):

                print("Recognition cancelled.")

                return "UNKNOWN"

        # ----------------------------------------------------
        # MAJORITY VOTING
        # ----------------------------------------------------

        counts = Counter(
            vote for vote in votes
            if vote != "UNKNOWN"
        )

        print("\nRecognition results:")
        print(dict(counts))

        if not counts:

            print("No valid gesture detected.")

            return "UNKNOWN"

        best_gesture, best_votes = counts.most_common(1)[0]

        print(
            f"Best result: {best_gesture} "
            f"({best_votes}/{NUMBER_OF_FRAMES})"
        )

        if best_votes >= MINIMUM_VOTES:

            print(f"Final result: {best_gesture}")

            return best_gesture

        else:

            print("Not enough agreement between frames.")

            return "UNKNOWN"


    # ========================================================
    # CLOSE CAMERA
    # ========================================================

    def close(self):

        self.cap.release()

        cv2.destroyAllWindows()

        self.landmarker.close()

        print("Camera recognizer closed.")


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    camera = None

    try:

        camera = CameraRecognizer()

        while True:

            print("\nReady for a new round!")

            input(
                "Press ENTER when the player has made "
                "their gesture..."
            )

            player_move = camera.detect_player_move()

            print(
                "\nPLAYER MOVE:",
                player_move
            )

            again = input(
                "\nTest another round? (y/n): "
            )

            if again.lower() != "y":
                break

    except Exception as error:

        print("ERROR:", error)

    finally:

        if camera is not None:
            camera.close()