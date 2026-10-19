
import cv2
import mediapipe as mp
import os
import urllib.request

MODEL_PATH = "hand_landmarker.task"

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/"
    "hand_landmarker.task"
)

if not os.path.exists(MODEL_PATH):
    print("Laddar ner handmodellen...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


def finger_is_extended(landmarks, tip, pip):
    """
    Enkel kontroll av om ett finger är utsträckt.
    Fungerar bäst när handflatan är vänd mot kameran
    och fingrarna pekar uppåt i bilden.
    """
    return landmarks[tip].y < landmarks[pip].y


def recognize_gesture(landmarks):
    """
    Returnerar rock, scissors, paper eller unknown.
    Landmarks är MediaPipes 21 handpunkter.
    """

    # Pekfinger, långfinger, ringfinger och lillfinger.
    # Varje finger kontrolleras genom fingertopp och led.
    index = finger_is_extended(landmarks, 8, 6)
    middle = finger_is_extended(landmarks, 12, 10)
    ring = finger_is_extended(landmarks, 16, 14)
    pinky = finger_is_extended(landmarks, 20, 18)

    extended_count = sum([index, middle, ring, pinky])

    # Alla fyra fingrarna utsträckta = påse
    if extended_count == 4:
        return "PAPER"

    # Pekfinger och långfinger utsträckta,
    # ringfinger och lillfinger böjda = sax
    if index and middle and not ring and not pinky:
        return "SCISSORS"

    # Inga av de fyra fingrarna utsträckta = sten
    if extended_count == 0:
        return "ROCK"

    return "UNKNOWN"


BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

with HandLandmarker.create_from_options(options) as landmarker:
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Kunde inte öppna kameran.")
        raise SystemExit

    print("Visa sten, sax eller påse. Tryck Q för att avsluta.")

    while True:
        success, frame = camera.read()

        if not success:
            print("Kunde inte läsa kamerabilden.")
            break

        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp_ms = int(
            cv2.getTickCount() / cv2.getTickFrequency() * 1000
        )

        result = landmarker.detect_for_video(
            mp_image,
            timestamp_ms
        )

        gesture = "NO HAND"

        if result.hand_landmarks:
            landmarks = result.hand_landmarks[0]
            gesture = recognize_gesture(landmarks)

            height, width, _ = frame.shape

            points = [
                (int(point.x * width), int(point.y * height))
                for point in landmarks
            ]

            for x, y in points:
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            connections = (
                mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS
            )

            for connection in connections:
                cv2.line(
                    frame,
                    points[connection.start],
                    points[connection.end],
                    (255, 100, 0),
                    2
                )

        cv2.putText(
            frame,
            f"Gesture: {gesture}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Rock Paper Scissors", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
