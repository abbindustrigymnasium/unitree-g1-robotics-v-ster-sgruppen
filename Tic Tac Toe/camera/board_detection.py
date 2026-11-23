import cv2
import numpy as np


class BoardDetector:
    """
    Detects four ArUco markers and uses their CENTRES as the board corners.

    Required marker layout when looking at the board from above:
        ID 0 = top-left
        ID 1 = top-right
        ID 2 = bottom-right
        ID 3 = bottom-left

    Place each marker so its centre sits exactly on the corresponding
    outer corner of the tic-tac-toe board. Keep all four markers visible.
    """

    def __init__(self):
        if not hasattr(cv2, "aruco"):
            raise RuntimeError(
                "cv2.aruco is missing. Install opencv-contrib-python, "
                "not just opencv-python."
            )

        self.dictionary = cv2.aruco.getPredefinedDictionary(
            cv2.aruco.DICT_4X4_50
        )

        if hasattr(cv2.aruco, "ArucoDetector"):
            parameters = cv2.aruco.DetectorParameters()
            self.detector = cv2.aruco.ArucoDetector(
                self.dictionary, parameters
            )
            self.old_api = False
        else:
            self.parameters = cv2.aruco.DetectorParameters_create()
            self.detector = None
            self.old_api = True

    def detect(self, frame):
        """Return (ordered_corner_points, detected_marker_ids)."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.old_api:
            marker_corners, marker_ids, _ = cv2.aruco.detectMarkers(
                gray, self.dictionary, parameters=self.parameters
            )
        else:
            marker_corners, marker_ids, _ = self.detector.detectMarkers(gray)

        if marker_ids is None:
            return None, []

        marker_ids = marker_ids.flatten().tolist()
        centres_by_id = {}

        for corners, marker_id in zip(marker_corners, marker_ids):
            if marker_id in (0, 1, 2, 3):
                # Each marker has four image corners. Their mean is its centre.
                centres_by_id[marker_id] = corners.reshape(4, 2).mean(axis=0)

        if not all(marker_id in centres_by_id for marker_id in (0, 1, 2, 3)):
            return None, marker_ids

        ordered = np.float32([
            centres_by_id[0],  # top-left
            centres_by_id[1],  # top-right
            centres_by_id[2],  # bottom-right
            centres_by_id[3],  # bottom-left
        ])

        return ordered, marker_ids

    @staticmethod
    def draw_corners(frame, corners):
        if corners is None:
            return frame

        points = corners.astype(int)
        for index, point in enumerate(points):
            cv2.circle(frame, tuple(point), 8, (0, 255, 0), -1)
            cv2.putText(
                frame, str(index), tuple(point + np.array([10, -10])),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
            )

        cv2.polylines(frame, [points], True, (255, 0, 0), 2)
        return frame
