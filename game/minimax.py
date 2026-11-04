import random
from functools import lru_cache

from game.rules import (
    EMPTY,
    HUMAN,
    ROBOT,
    get_winner,
    get_player_moves,
)


SEARCH_DEPTH = 5


def apply_move(board, move, player):
    """
    Return a NEW board with the move applied.
    Does not modify the original board.
    """

    source, destination = move

    new_board = [row.copy() for row in board]

    if source is not None:
        sr, sc = source
        new_board[sr][sc] = EMPTY

    dr, dc = destination
    new_board[dr][dc] = player

    return new_board


def evaluate(board):
    """
    Evaluate a non-terminal position.
    Positive = good for robot.
    Negative = good for human.
    """

    lines = []

    lines.extend(board)

    for c in range(3):
        lines.append([board[r][c] for r in range(3)])

    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2-i] for i in range(3)])

    score = 0

    for line in lines:
        robot_count = line.count(ROBOT)
        human_count = line.count(HUMAN)

        if robot_count > 0 and human_count > 0:
            continue

        if robot_count == 2:
            score += 10
        elif robot_count == 1:
            score += 1

        if human_count == 2:
            score -= 10
        elif human_count == 1:
            score -= 1

    return score


@lru_cache(maxsize=200000)
def minimax(board_tuple, depth, maximizing):
    board = [list(row) for row in board_tuple]

    winner = get_winner(board)

    if winner == ROBOT:
        return 1000 + depth

    if winner == HUMAN:
        return -1000 - depth

    if depth == 0:
        return evaluate(board)

    player = ROBOT if maximizing else HUMAN

    moves = get_player_moves(board, player)

    if not moves:
        return 0

    if maximizing:
        best = float("-inf")

        for move in moves:
            new_board = apply_move(board, move, ROBOT)

            new_tuple = tuple(
                tuple(row) for row in new_board
            )

            score = minimax(
                new_tuple,
                depth - 1,
                False
            )

            best = max(best, score)

        return best

    else:
        best = float("inf")

        for move in moves:
            new_board = apply_move(board, move, HUMAN)

            new_tuple = tuple(
                tuple(row) for row in new_board
            )

            score = minimax(
                new_tuple,
                depth - 1,
                True
            )

            best = min(best, score)

        return best


def choose_best_move(board):
    """
    Return the robot's best move.

    Format:
    (source, destination)

    source=None during placement.
    """

    if get_winner(board) is not None:
        return None

    moves = get_player_moves(board, ROBOT)

    if not moves:
        return None

    best_move = None
    best_score = float("-inf")

    for move in moves:
        new_board = apply_move(board, move, ROBOT)

        board_tuple = tuple(
            tuple(row) for row in new_board
        )

        score = minimax(
            board_tuple,
            SEARCH_DEPTH,
            False
        )

        if score > best_score:
            best_score = score
            best_move = move

    return best_move

def find_winning_moves(board, player):
    """
    Find moves that would immediately win the game.
    """

    winning_moves = []

    for move in get_player_moves(board, player):
        new_board = apply_move(board, move, player)

        if get_winner(new_board) == player:
            winning_moves.append(move)

    return winning_moves


def move_priority(board, move):
    """
    Give moves a simple strategic priority.
    """

    source, destination = move
    row, col = destination

    score = 0

    # Prefer center
    if (row, col) == (1, 1):
        score += 3

    # Prefer corners
    elif (row, col) in [
        (0, 0), (0, 2),
        (2, 0), (2, 2)
    ]:
        score += 2

    # Prefer moves that create two in a row
    new_board = apply_move(board, move, ROBOT)

    score += evaluate(new_board) * 0.2

    return score


def choose_move(board, difficulty):
    """
    Human-like AI with adjustable difficulty.
    """

    settings = {
        "easy": {
            "block_chance": 0.45,
            "best_move_chance": 0.20
        },
        "medium": {
            "block_chance": 0.75,
            "best_move_chance": 0.50
        },
        "hard": {
            "block_chance": 0.95,
            "best_move_chance": 0.80
        },
        "expert": {
            "block_chance": 1.00,
            "best_move_chance": 1.00
        }
    }

    if difficulty not in settings:
        raise ValueError("Invalid difficulty")

    moves = get_player_moves(board, ROBOT)

    if not moves:
        return None

    config = settings[difficulty]

    # 1. Always take an immediate winning move
    winning_moves = find_winning_moves(board, ROBOT)

    if winning_moves:
        return random.choice(winning_moves)

    # 2. Check if human has an immediate winning move
    human_winning_moves = find_winning_moves(board, HUMAN)

    if human_winning_moves:

        # Find robot moves that prevent the human
        # from winning immediately
        blocking_moves = []

        for move in moves:

            new_board = apply_move(board, move, ROBOT)

            remaining_threats = find_winning_moves(
                new_board, HUMAN
            )

            if not remaining_threats:
                blocking_moves.append(move)

        if blocking_moves and random.random() < config["block_chance"]:
            return max(
                blocking_moves,
                key=lambda move: move_priority(board, move)
            )

    # 3. Sometimes use full minimax
    if random.random() < config["best_move_chance"]:
        return choose_best_move(board)

    # 4. Otherwise choose a reasonable move
    scored_moves = [
        (move, move_priority(board, move))
        for move in moves
    ]

    # Sort moves by strategic priority
    scored_moves.sort(
        key=lambda item: item[1],
        reverse=True
    )

    # Select from the top 3 moves
    top_moves = [
        move for move, score in scored_moves[:3]
    ]

    return random.choice(top_moves)