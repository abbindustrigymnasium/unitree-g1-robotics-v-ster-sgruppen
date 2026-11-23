# Tic-tac-toe camera

## What this first version does

1. Reads the camera using OpenCV (RTSP URL or local camera index).
2. Detects four ArUco markers.
3. Uses their centres to rectify the board into a top-down square.
4. Attempts to classify each cell as X, O, empty, or UNKNOWN.
5. Shows the original camera image and rectified board.

This version does not decide whose turn it is, choose a move, or control the robot.

## Marker setup

Print four markers from OpenCV's `DICT_4X4_50` dictionary:
- ID 0: top-left board corner
- ID 1: top-right board corner
- ID 2: bottom-right board corner
- ID 3: bottom-left board corner

Place each marker so its centre is exactly at the corresponding outer corner
of the board. Keep all four markers visible. The marker centres define the
board quadrilateral.

The first version assumes dark X/O marks on a light board. Recognition will
need tuning for the actual board, pieces, lighting, and camera angle.

## Install

Use the Python environment used by the project:

```bash
pip install -r requirements.txt
```

If `cv2.aruco` is missing, make sure `opencv-python` and
`opencv-contrib-python` are not installed together in the same environment.
Use `opencv-contrib-python`.

## Run

For the G1 RTSP camera, set `CAMERA_SOURCE` to the same URL used by the RPS
camera, for example:

```bash
export CAMERA_SOURCE="rtsp://YOUR_G1_IP:8554/cam"
python -m camera.camera
```

For a local webcam:

```bash
export CAMERA_SOURCE=0
python -m camera.camera
```

Run from the project root so Python can import the `camera` package.

## Important

The four-marker-centre layout is a calibration convention. The markers must
be placed consistently as described above. If you instead place markers
outside the board or use a different printed layout, the corner mapping must
be changed.
