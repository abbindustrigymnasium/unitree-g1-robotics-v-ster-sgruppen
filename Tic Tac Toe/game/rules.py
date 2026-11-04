EMPTY = ""
HUMAN = "X"
ROBOT = "O"

MAX_PIECES = 3


def get_winner(board):
    lines = []

    # Rows
    lines.extend(board)

    # Columns
    for col in range(3):
        lines.append([
            board[row][col]
            for row in range(3)
        ])

    # Diagonals
    lines.append([
        board[0][0],
        board[1][1],
        board[2][2]
    ])

    lines.append([
        board[0][2],
        board[1][1],
        board[2][0]
    ])

    for line in lines:
        if line[0] != EMPTY and all(
            cell == line[0] for cell in line
        ):
            return line[0]

    return None


def count_pieces(board, player):
    return sum(
        row.count(player)
        for row in board
    )


def get_available_moves(board):
    return [
        (r, c)
        for r in range(3)
        for c in range(3)
        if board[r][c] == EMPTY
    ]


def get_player_moves(board, player):
    """
    Returns legal moves.

    Placement: (None, destination)
    Movement: (source, destination)
    """

    if get_winner(board) is not None:
        return []

    empty = get_available_moves(board)

    # Phase 1: Player has fewer than 3 pieces
    if count_pieces(board, player) < MAX_PIECES:
        return [
            (None, destination)
            for destination in empty
        ]

    # Phase 2: Move existing pieces
    moves = []

    for r in range(3):
        for c in range(3):
            if board[r][c] == player:

                for destination in empty:
                    moves.append(
                        ((r, c), destination)
                    )

    return moves


def is_game_over(board):
    return get_winner(board) is not None