import os

# Camera source
CAMERA_SOURCE = os.getenv("CAMERA_SOURCE", "0")

# Camera resolution
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Board settings
BOARD_SIZE = 600
BOARD_CELLS = 3

# ArUco settings
ARUCO_MARKER_IDS = [0, 1, 2, 3]