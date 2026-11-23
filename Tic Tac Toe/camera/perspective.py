import cv2
import numpy as np


class BoardPerspective:
    def __init__(self, board_size=600):
        self.board_size = board_size

    def warp(self, frame, source_corners):
        """Rectify the board into a square top-down image."""
        size = self.board_size

        destination = np.float32([
            [0, 0],
            [size - 1, 0],
            [size - 1, size - 1],
            [0, size - 1],
        ])

        matrix = cv2.getPerspectiveTransform(
            np.float32(source_corners), destination
        )

        warped = cv2.warpPerspective(frame, matrix, (size, size))
        return warped, matrix

    def cell_bounds(self, row, col):
        cell_size = self.board_size // 3
        x1 = col * cell_size
        y1 = row * cell_size
        return x1, y1, x1 + cell_size, y1 + cell_size
