import cv2

for i in range(5):

    camera = cv2.VideoCapture(i)

    if camera.isOpened():

        ret, frame = camera.read()

        if ret:
            print(f"Camera {i}: WORKING")
        else:
            print(f"Camera {i}: opened, but couldn't read image")

    else:
        print(f"Camera {i}: unavailable")

    camera.release()