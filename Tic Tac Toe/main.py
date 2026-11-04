from game.board import create_board, make_move

from game.rules import (
    HUMAN,
    ROBOT,
    count_pieces,
    get_winner,
)

from game.minimax import choose_move


def print_board(board):
    print()

    for i, row in enumerate(board):
        print(" | ".join(
            cell if cell else " "
            for cell in row
        ))

        if i < 2:
            print("---------")

    print()


def get_input_position(prompt):
    while True:
        try:
            text = input(prompt)
            parts = text.split()

            if len(parts) != 2:
                print("Enter row and column, e.g. 1 2")
                continue

            row, col = map(int, parts)

            if row in range(1, 4) and col in range(1, 4):
                return row - 1, col - 1

            print("Coordinates must be 1, 2 or 3.")

        except ValueError:
            print("Invalid input.")


def main():
    board = create_board()

    print("Choose difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("4. Expert")

    difficulties = {
        "1": "easy",
        "2": "medium",
        "3": "hard",
        "4": "expert"
    }

    while True:
        choice = input("Difficulty (1-4): ")

        if choice in difficulties:
            difficulty = difficulties[choice]
            break

        print("Invalid choice. Try again.")

    print("SWEDISH TIC TAC TOE")
    print("You are X. Robot is O.")
    print("Each player has 3 pieces.")
    print("Enter row and column from 1 to 3 (e.g. 1 3).")

    current_player = HUMAN

    # Track repeated positions to prevent endless games.
    position_counts = {}

    while True:

        print_board(board)

        winner = get_winner(board)

        if winner:
            if winner == HUMAN:
                print(f"You win!")
            else:
                print(f"AI wins!")
            break

        # Same position + same player to move
        state = (
            tuple(tuple(row) for row in board),
            current_player
        )

        position_counts[state] = (
            position_counts.get(state, 0) + 1
        )

        if position_counts[state] >= 3:
            print("Draw! Position repeated three times.")
            break

        if current_player == HUMAN:

            if count_pieces(board, HUMAN) < 3:

                print("PLACE a new X")

                while True:
                    row, col = get_input_position(
                        "Destination (row col): "
                    )

                    if make_move(
                        board, row, col, HUMAN
                    ):
                        break

                    print("Invalid move.")

            else:

                print("MOVE one of your X pieces")

                while True:
                    source = get_input_position(
                        "Pick up from (row col): "
                    )

                    destination = get_input_position(
                        "Move to (row col): "
                    )

                    if make_move(
                        board,
                        destination[0],
                        destination[1],
                        HUMAN,
                        source=source
                    ):
                        break

                    print("Invalid move. Try again.")

        else:

            move = choose_move(board, difficulty=difficulty)    

            if move is None:
                print("Robot has no legal move.")
                break

            source, destination = move

            make_move(
                board,
                destination[0],
                destination[1],
                ROBOT,
                source=source
            )

            if source is None:
                print(
                    f"Robot places O at {(destination[0] + 1, destination[1] + 1)}"
                )
            else:
                print(
                    f"Robot moves O from "
                    f"{(source[0] + 1, source[1] + 1)} to "
                    f"{(destination[0] + 1, destination[1] + 1)}"
                )

        current_player = (
            ROBOT if current_player == HUMAN else HUMAN
        )


if __name__ == "__main__":
    main()
