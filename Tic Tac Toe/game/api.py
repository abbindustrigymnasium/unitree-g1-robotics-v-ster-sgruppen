from game.board import validate_board
from game.minimax import choose_move
from game.rules import HUMAN, ROBOT, get_winner, count_pieces


VALID_DIFFICULTIES = ("easy", "medium", "hard", "expert")


def get_robot_move(board, difficulty):
    """
    Public interface for Group 3.

    Returns:
        (source, destination)

    Raises:
        ValueError if the board or difficulty is invalid.
    """

    # 1. Validate difficulty
    if difficulty not in VALID_DIFFICULTIES:
        raise ValueError(
            f"Invalid difficulty: {difficulty}"
        )

    # 2. Validate board
    if not validate_board(board):
        raise ValueError("Invalid board state")

    # 3. Check if the game is already finished
    if get_winner(board) is not None:
        return None

    # 4. Make sure it is the robot's turn
    x_count = count_pieces(board, HUMAN)
    o_count = count_pieces(board, ROBOT)

    # During placement, X always plays first.
    if x_count < 3 or o_count < 3:
        if x_count != o_count + 1:
            raise ValueError("It is not the robot's turn")

    # During movement, both have 3 pieces.
    # Group 3 must track whose turn it is.

    # 5. Get the robot's move
    return choose_move(board, difficulty=difficulty)