import cv2
import numpy as np


class PieceRecognizer:
    """
    Basic recognizer for dark, hand-drawn X and O symbols on a light board.

    This is a starting implementation, not a trained classifier. It returns
    UNKNOWN rather than guessing when a cell is ambiguous.
    """

    def __init__(self, board_size=600):
        self.board_size = board_size

    def _classify_cell(self, cell):
        height, width = cell.shape[:2]

        # Ignore the outer part of each cell so grid lines are less likely
        # to be mistaken for pieces.
        margin_x = int(width * 0.20)
        margin_y = int(height * 0.20)
        roi = cell[
            margin_y:height - margin_y,
            margin_x:width - margin_x
        ]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # Assumes dark symbols on a light board.
        _, binary = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        )

        # Remove tiny noise.
        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(
            binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return ""

        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        roi_area = roi.shape[0] * roi.shape[1]

        # Ignore small specks.
        if area < roi_area * 0.015:
            return ""

        x, y, w, h = cv2.boundingRect(largest)
        if h == 0 or w == 0:
            return "UNKNOWN"

        aspect = w / h
        perimeter = cv2.arcLength(largest, True)
        circularity = (
            4 * np.pi * area / (perimeter * perimeter)
            if perimeter > 0 else 0
        )

        # O: roughly round contour with a hole.
        contour_mask = np.zeros(binary.shape, dtype=np.uint8)
        cv2.drawContours(contour_mask, [largest], -1, 255, -1)
        contours_with_holes, hierarchy = cv2.findContours(
            binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        )

        has_hole = (
            hierarchy is not None
            and any(hierarchy[0][i][3] != -1 for i in range(len(contours_with_holes)))
        )

        if 0.65 <= aspect <= 1.35 and circularity > 0.45 and has_hole:
            return "O"

        # X: look for two substantial diagonal line segments crossing.
        edges = cv2.Canny(binary, 50, 150)
        lines = cv2.HoughLinesP(
            edges, 1, np.pi / 180, threshold=12,
            minLineLength=max(12, min(w, h) // 3),
            maxLineGap=12
        )

        diagonal_a = False
        diagonal_b = False

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                dx = x2 - x1
                dy = y2 - y1
                if dx == 0:
                    continue

                slope = dy / dx
                if 0.45 < slope < 2.5:
                    diagonal_a = True
                elif -2.5 < slope < -0.45:
                    diagonal_b = True

        if diagonal_a and diagonal_b:
            return "X"

        return "UNKNOWN"

    def recognize(self, warped_board):
        """Return a 3x3 list containing X, O, empty string, or UNKNOWN."""
        board = []
        cell_size = self.board_size // 3

        for row in range(3):
            board_row = []

            for col in range(3):
                x1 = col * cell_size
                y1 = row * cell_size
                cell = warped_board[
                    y1:y1 + cell_size,
                    x1:x1 + cell_size
                ]
                board_row.append(self._classify_cell(cell))

            board.append(board_row)

        return board

    @staticmethod
    def draw_board_state(image, board):
        cell_size = image.shape[0] // 3

        for row in range(3):
            for col in range(3):
                value = board[row][col]
                if value == "":
                    value = "-"
                x = col * cell_size + 18
                y = row * cell_size + 38

                cv2.putText(
                    image, value, (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                    (0, 0, 255) if value == "UNKNOWN" else (0, 180, 0),
                    2
                )

        return image
