
import cv2
import mediapipe as mp
import urllib.request
import os

# Hämta MediaPipes färdiga modell om den inte redan finns
MODEL_PATH = "hand_landmarker.task"
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/"
    "hand_landmarker.task"
)

if not os.path.exists(MODEL_PATH):
    print("Laddar ner handmodellen...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("Modellen är nedladdad!")

# Ställ in MediaPipe
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1
)

# Starta handigenkänningen
with HandLandmarker.create_from_options(options) as landmarker:

    # Öppna kameran
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Kunde inte öppna kameran.")
        exit()

    print("Visa handen för kameran. Tryck Q för att avsluta.")

    while True:
        success, frame = camera.read()

        if not success:
            print("Kunde inte läsa från kameran.")
            break

        # Spegelvänd bilden så det känns naturligt
        frame = cv2.flip(frame, 1)

        # Konvertera från OpenCV-format till RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Gör om bilden till ett MediaPipe-objekt
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Tidsstämpel i millisekunder
        timestamp_ms = int(
            cv2.getTickCount() / cv2.getTickFrequency() * 1000
        )

        # Hitta handen
        result = landmarker.detect_for_video(
            mp_image,
            timestamp_ms
        )

        # Rita ut handens 21 punkter
        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                height, width, _ = frame.shape

                points = []

                for landmark in hand_landmarks:
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    points.append((x, y))

                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 255, 0),
                        -1
                    )

                # Rita linjer mellan punkterna
                connections = (
                    mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS
                )

                for connection in connections:
                    start = points[connection.start]
                    end = points[connection.end]

                    cv2.line(
                        frame,
                        start,
                        end,
                        (255, 100, 0),
                        2
                    )

            cv2.putText(
                frame,
                "HAND DETECTED",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
        else:
            cv2.putText(
                frame,
                "No hand detected",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        # Visa resultatet
        cv2.imshow("Hand Tracking - Sten Sax Pase", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
