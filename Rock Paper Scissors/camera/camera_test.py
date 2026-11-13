
import cv2

from camera_recognition import CameraRecognizer


print("OpenCV version:", cv2.__version__)

camera = None

try:
    camera = CameraRecognizer()

    while True:
        success, frame = camera.read_latest_frame()

        if not success or frame is None:
            print("Could not read camera.")
            break

        frame = cv2.flip(frame, 1)
        gesture, display_frame = camera.process_frame(frame)

        cv2.putText(
            display_frame,
            f"Prediction: {gesture}",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("Rock Paper Scissors Camera", display_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    if camera is not None:
        camera.close()
