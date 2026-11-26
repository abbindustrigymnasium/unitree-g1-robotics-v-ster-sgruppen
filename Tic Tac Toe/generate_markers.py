import cv2
import os

# Create a folder for the markers
os.makedirs("markers", exist_ok=True)

# Use the same ArUco dictionary as the camera
dictionary = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_4X4_50
)

# Generate markers 0, 1, 2 and 3
for marker_id in range(4):

    marker = cv2.aruco.generateImageMarker(
        dictionary,
        marker_id,
        400
    )

    filename = f"markers/marker_{marker_id}.png"

    cv2.imwrite(filename, marker)

    print(f"Created: {filename}")

print("All markers generated!")