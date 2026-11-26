
import cv2
import numpy as np


class PieceRecognizer:
    """
    Colour-based Tic Tac Toe piece recognition.

    Red  = X (Human)
    Blue = O (Robot)
    ""   = Empty
    UNKNOWN = Uncertain detection
    """

    def __init__(self, board_size=600):
        self.board_size = board_size

        # Minimum percentage of coloured pixels
        # required to recognise a piece.
        self.min_color_ratio = 0.015

        # Minimum saturation required.
        # This helps ignore grey shadows and reflections.
        self.min_saturation = 80

        # Minimum brightness.
        self.min_brightness = 50

    # ======================================================
    # Create colour masks
    # ======================================================

    def _get_color_masks(self, roi):

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # RED
        # Red exists on both ends of the HSV hue scale.

        lower_red_1 = np.array([0, self.min_saturation, self.min_brightness])
        upper_red_1 = np.array([12, 255, 255])

        lower_red_2 = np.array([168, self.min_saturation, self.min_brightness])
        upper_red_2 = np.array([180, 255, 255])

        red_mask_1 = cv2.inRange(
            hsv,
            lower_red_1,
            upper_red_1
        )

        red_mask_2 = cv2.inRange(
            hsv,
            lower_red_2,
            upper_red_2
        )

        red_mask = cv2.bitwise_or(
            red_mask_1,
            red_mask_2
        )

        # BLUE

        lower_blue = np.array([90, self.min_saturation, self.min_brightness])
        upper_blue = np.array([135, 255, 255])

        blue_mask = cv2.inRange(
            hsv,
            lower_blue,
            upper_blue
        )

        return red_mask, blue_mask

    # ======================================================
    # Clean colour masks
    # ======================================================

    def _clean_mask(self, mask):

        kernel = np.ones((3, 3), np.uint8)

        # Remove small noise
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel
        )

        # Connect nearby coloured pixels
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel
        )

        return mask

    # ======================================================
    # Classify one cell
    # ======================================================

    def _classify_cell(self, cell):

        height, width = cell.shape[:2]

        if height == 0 or width == 0:
            return "UNKNOWN"

        # Ignore cell edges to avoid detecting grid lines.
        margin_x = int(width * 0.20)
        margin_y = int(height * 0.20)

        roi = cell[
            margin_y:height - margin_y,
            margin_x:width - margin_x
        ]

        if roi.size == 0:
            return "UNKNOWN"

        # Detect red and blue
        red_mask, blue_mask = self._get_color_masks(roi)

        # Remove noise
        red_mask = self._clean_mask(red_mask)
        blue_mask = self._clean_mask(blue_mask)

        # Calculate percentage of coloured pixels
        total_pixels = roi.shape[0] * roi.shape[1]

        red_pixels = cv2.countNonZero(red_mask)
        blue_pixels = cv2.countNonZero(blue_mask)

        red_ratio = red_pixels / total_pixels
        blue_ratio = blue_pixels / total_pixels

        # ==================================================
        # Check for RED X
        # ==================================================

        red_detected = red_ratio >= self.min_color_ratio

        # ==================================================
        # Check for BLUE O
        # ==================================================

        blue_detected = blue_ratio >= self.min_color_ratio

        # ==================================================
        # Classification
        # ==================================================

        # Both colours detected:
        # The cell may contain multiple objects or noise.

        if red_detected and blue_detected:

            return "UNKNOWN"

        if red_detected:

            return "X"

        if blue_detected:

            return "O"

        # No significant red or blue detected.
        # Therefore, the cell is empty.

        return ""

    # ======================================================
    # Analyze the entire board
    # ======================================================

    def recognize(self, warped_board):
        """
        Return a 3x3 list containing:

        X       = Red piece (Human)
        O       = Blue piece (Robot)
        ""      = Empty cell
        UNKNOWN = Uncertain detection
        """

        board = []

        height, width = warped_board.shape[:2]

        cell_width = width // 3
        cell_height = height // 3

        for row in range(3):

            board_row = []

            for col in range(3):

                x1 = col * cell_width
                y1 = row * cell_height

                # Make sure the final row/column
                # includes any remaining pixels.

                x2 = (col + 1) * cell_width if col < 2 else width
                y2 = (row + 1) * cell_height if row < 2 else height

                cell = warped_board[y1:y2, x1:x2]

                result = self._classify_cell(cell)

                board_row.append(result)

            board.append(board_row)

        return board

    # ======================================================
    # Draw detected board state
    # ======================================================

    @staticmethod
    def draw_board_state(image, board):

        height, width = image.shape[:2]

        cell_width = width // 3
        cell_height = height // 3

        for row in range(3):

            for col in range(3):

                value = board[row][col]

                if value == "":
                    value = "-"

                x = col * cell_width + 18
                y = row * cell_height + 38

                # Green = detected
                # Red = uncertain

                if value == "UNKNOWN":
                    color = (0, 0, 255)

                elif value == "X":
                    color = (0, 0, 255)

                elif value == "O":
                    color = (255, 0, 0)

                else:
                    color = (0, 180, 0)

                cv2.putText(
                    image,
                    value,
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    color,
                    2
                )

        return image