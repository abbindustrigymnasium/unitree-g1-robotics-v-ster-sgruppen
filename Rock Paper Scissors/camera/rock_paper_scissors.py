
import cv2
import mediapipe as mp
import os
import urllib.request
import math
import time


# ============================================================
# SETTINGS
# ============================================================

MODEL_PATH = "hand_landmarker.task"

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/"
    "hand_landmarker.task"
)


# ============================================================
# DOWNLOAD MODEL IF NEEDED
# ============================================================

if not os.path.exists(MODEL_PATH):
    print("Downloading hand model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Download complete!")


# ============================================================
# MEDIAPIPE SETUP
# ============================================================

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)

landmarker = HandLandmarker.create_from_options(options)


# ============================================================
# ANGLE CALCULATION
# ============================================================

def angle_3d(a, b, c):
    """Calculate the angle ABC using 3D hand landmarks."""

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

    dot = sum(ba[i] * bc[i] for i in range(3))

    mag_ba = math.sqrt(sum(v * v for v in ba))
    mag_bc = math.sqrt(sum(v * v for v in bc))

    if mag_ba == 0 or mag_bc == 0:
        return 0

    cosine = dot / (mag_ba * mag_bc)
    cosine = max(-1, min(1, cosine))

    return math.degrees(math.acos(cosine))


# ============================================================
# FINGER DETECTION
# ============================================================

def finger_angles(landmarks, mcp, pip, dip, tip):
    """Return the PIP and DIP joint angles for a finger."""

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
    """Estimate whether a finger is extended."""

    pip_angle, dip_angle = finger_angles(
        landmarks, mcp, pip, dip, tip
    )

    return pip_angle > 120 and dip_angle > 130


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

    ring_pip, ring_dip = finger_angles(
        landmarks, 13, 14, 15, 16
    )

    extended_count = sum([index, middle, ring, pinky])

    # SCISSORS:
    # Prioritize index and middle fingers.
    # The ring finger does not need to be curled.
    if index and middle and not pinky:
        gesture = "SCISSORS"

    # PAPER:
    # All four fingers are detected as extended.
    elif extended_count == 4:
        gesture = "PAPER"

    # ROCK:
    # None of the four fingers are detected as extended.
    elif extended_count == 0:
        gesture = "ROCK"

    else:
        gesture = "UNKNOWN"

    debug = {
        "Index": index,
        "Middle": middle,
        "Ring": ring,
        "Pinky": pinky,
        "Ring PIP": round(ring_pip, 1),
        "Ring DIP": round(ring_dip, 1),
    }

    return gesture, debug


# ============================================================
# DRAW HAND LANDMARKS
# ============================================================

# Manually defined connections so we don't need mp.solutions.
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
# CAMERA SETUP
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open camera.")
    landmarker.close()
    raise SystemExit


print("\nCamera started!")
print("Press Q to quit.\n")

start_time = time.monotonic()
last_timestamp_ms = -1


# ============================================================
# MAIN LOOP
# ============================================================

try:
    while True:

        success, frame = cap.read()

        if not success:
            print("Could not read camera frame.")
            break

        # Mirror the image
        frame = cv2.flip(frame, 1)

        # Convert image to RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Ensure timestamps always increase
        timestamp_ms = int(
            (time.monotonic() - start_time) * 1000
        )

        timestamp_ms = max(
            timestamp_ms,
            last_timestamp_ms + 1
        )

        last_timestamp_ms = timestamp_ms

        result = landmarker.detect_for_video(
            mp_image,
            timestamp_ms
        )

        gesture = "NO HAND"
        debug = {}

        # ----------------------------------------------------
        # PROCESS HAND
        # ----------------------------------------------------

        if result.hand_landmarks:

            landmarks_2d = result.hand_landmarks[0]
            landmarks_3d = result.hand_world_landmarks[0]

            gesture, debug = recognize_gesture(
                landmarks_3d
            )

            # Draw hand landmarks and connections
            draw_hand(frame, landmarks_2d)

            # Show finger detection values
            debug_text = (
                f"I:{int(debug['Index'])} "
                f"M:{int(debug['Middle'])} "
                f"R:{int(debug['Ring'])} "
                f"P:{int(debug['Pinky'])}"
            )

            cv2.putText(
                frame,
                debug_text,
                (10, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 0),
                2
            )

            # Show ring finger angles
            ring_text = (
                f"Ring PIP: {debug['Ring PIP']} "
                f"DIP: {debug['Ring DIP']}"
            )

            cv2.putText(
                frame,
                ring_text,
                (10, 105),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 0),
                2
            )

            # Print results to terminal
            print(
                f"Gesture: {gesture:8} | "
                f"Index: {debug['Index']} | "
                f"Middle: {debug['Middle']} | "
                f"Ring: {debug['Ring']} | "
                f"Pinky: {debug['Pinky']} | "
                f"Ring PIP: {debug['Ring PIP']} | "
                f"Ring DIP: {debug['Ring DIP']}"
            )

        # ----------------------------------------------------
        # DISPLAY GESTURE
        # ----------------------------------------------------

        cv2.putText(
            frame,
            f"Gesture: {gesture}",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "Rock Paper Scissors Recognition",
            frame
        )

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    landmarker.close()
