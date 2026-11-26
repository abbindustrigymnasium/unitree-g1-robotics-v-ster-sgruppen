import cv2

# Try opening the webcam using DirectShow instead of MSMF
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not camera.isOpened():
    print("ERROR: Could not open webcam!")
    exit()

print("Webcam opened successfully!")

# Set resolution
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:

    ret, frame = camera.read()

    if not ret:
        print("Could not read frame")
        break

    cv2.imshow("Webcam Test", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()