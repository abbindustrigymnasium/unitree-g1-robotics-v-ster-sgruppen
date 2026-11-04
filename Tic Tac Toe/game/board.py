from game.rules import (
    EMPTY,
    HUMAN,
    ROBOT,
    get_player_moves,
)


def create_board():
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]


def make_move(board, row, col, player, source=None):
    """
    Apply a legal move.

    source=None means placing a new piece.

    source=(row, col) means moving an existing piece.

    Returns True if successful.
    """

    if player not in (HUMAN, ROBOT):
        return False

    move = (source, (row, col))

    if move not in get_player_moves(board, player):
        return False

    if source is not None:
        sr, sc = source
        board[sr][sc] = EMPTY

    board[row][col] = player

    return True

def validate_board(board):
    """
    Validate a Swedish tic-tac-toe board.

    Returns True if valid.
    Returns False if invalid.
    """

    # 1. Check board structure
    if not isinstance(board, list) or len(board) != 3:
        return False

    for row in board:
        if not isinstance(row, list) or len(row) != 3:
            return False

        for cell in row:
            if cell not in ("", "X", "O"):
                return False

    # 2. Count pieces
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)

    # Each player can have at most 3 pieces
    if x_count > 3 or o_count > 3:
        return False

    # Human plays first
    if x_count < o_count:
        return False

    # During placement, X can only have
    # one more piece than O
    if x_count - o_count > 1:
        return False

    # 3. Check whether both players have won
    winning_lines = []

    # Rows
    winning_lines.extend(board)

    # Columns
    for col in range(3):
        winning_lines.append([
            board[row][col]
            for row in range(3)
        ])

    # Diagonals
    winning_lines.append([
        board[0][0],
        board[1][1],
        board[2][2]
    ])

    winning_lines.append([
        board[0][2],
        board[1][1],
        board[2][0]
    ])

    x_wins = False
    o_wins = False

    for line in winning_lines:
        if line == ["X", "X", "X"]:
            x_wins = True

        if line == ["O", "O", "O"]:
            o_wins = True

    # Both players cannot win simultaneously
    if x_wins and o_wins:
        return False

    return True