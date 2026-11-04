def determine_winner(robot_move, player_move):
    """Determine the winner of a Rock Paper Scissors round.

    Returns "ROBOT", "PLAYER", or "DRAW"; returns "INVALID" for invalid moves.
    """
    valid_moves = ["ROCK", "PAPER", "SCISSORS"]

    if robot_move not in valid_moves or player_move not in valid_moves:
        return "INVALID"

    if robot_move == player_move:
        return "DRAW"

    winning_moves = {
        "ROCK": "SCISSORS",
        "PAPER": "ROCK",
        "SCISSORS": "PAPER",
    }

    if winning_moves[robot_move] == player_move:
        return "ROBOT"

    return "PLAYER"

