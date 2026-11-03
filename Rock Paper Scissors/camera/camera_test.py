
import cv2

print("OpenCV version:", cv2.__version__)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("ERROR: Camera could not open.")
    exit()

print("Camera opened successfully!")

while True:
    ret, frame = cap.read()

    if not ret or frame is None:
        print("Could not read camera.")
        break

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
