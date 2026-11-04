import unittest

from game.board import create_board, make_move, validate_board
from game.rules import (
    HUMAN,
    ROBOT,
    get_winner,
    count_pieces,
    get_player_moves,
)
from game.minimax import choose_move
from game.api import get_robot_move


class TestGame(unittest.TestCase):

    def test_invalid_too_many_pieces(self):
        board = [
            ["X", "X", "X"],
            ["X", "O", "O"],
            ["", "", ""]
        ]

        self.assertFalse(validate_board(board))


    def test_invalid_piece_counts(self):
        board = [
            ["O", "O", ""],
            ["X", "", ""],
            ["", "", ""]
        ]

        self.assertFalse(validate_board(board))


    def test_valid_movement_phase(self):
        board = [
            ["X", "O", "X"],
            ["O", "", "X"],
            ["", "O", ""]
        ]

        self.assertTrue(validate_board(board))

    def test_empty_board(self):
        board = create_board()

        self.assertEqual(count_pieces(board, HUMAN), 0)
        self.assertEqual(count_pieces(board, ROBOT), 0)
        self.assertIsNone(get_winner(board))

    def test_placing_piece(self):
        board = create_board()

        self.assertTrue(make_move(board, 0, 0, HUMAN))
        self.assertEqual(board[0][0], HUMAN)

    def test_cannot_place_on_occupied_square(self):
        board = create_board()

        make_move(board, 0, 0, HUMAN)

        self.assertFalse(make_move(board, 0, 0, ROBOT))

    def test_max_three_pieces(self):
        board = create_board()

        make_move(board, 0, 0, HUMAN)
        make_move(board, 0, 1, HUMAN)
        make_move(board, 1, 0, HUMAN)

        self.assertEqual(count_pieces(board, HUMAN), 3)

        # A fourth piece cannot be placed
        self.assertFalse(make_move(board, 2, 2, HUMAN))

    def test_moving_piece(self):
        board = create_board()

        make_move(board, 0, 0, HUMAN)
        make_move(board, 0, 1, HUMAN)
        make_move(board, 1, 0, HUMAN)

        success = make_move(
            board,
            2, 2,
            HUMAN,
            source=(0, 0)
        )

        self.assertTrue(success)
        self.assertEqual(board[0][0], "")
        self.assertEqual(board[2][2], HUMAN)

    def test_row_win(self):
        board = [
            ["X", "X", "X"],
            ["O", "", ""],
            ["", "", "O"]
        ]

        self.assertEqual(get_winner(board), HUMAN)

    def test_column_win(self):
        board = [
            ["O", "X", ""],
            ["O", "X", ""],
            ["O", "", "X"]
        ]

        self.assertEqual(get_winner(board), ROBOT)

    def test_diagonal_win(self):
        board = [
            ["X", "O", ""],
            ["", "X", "O"],
            ["", "", "X"]
        ]

        self.assertEqual(get_winner(board), HUMAN)

    def test_ai_returns_legal_move(self):
        board = [
            ["X", "", ""],
            ["", "O", ""],
            ["", "", ""]
        ]

        move = choose_move(board, difficulty="medium")

        legal_moves = get_player_moves(board, ROBOT)

        self.assertIn(move, legal_moves)

    def test_ai_does_not_change_board(self):
        board = [
            ["X", "", ""],
            ["", "O", ""],
            ["", "", ""]
        ]

        original = [row.copy() for row in board]

        choose_move(board, difficulty="medium")

        self.assertEqual(board, original)

    def test_api_rejects_invalid_board(self):
        board = [
            ["X", "X", "X"],
            ["X", "O", "O"],
            ["", "", ""]
        ]

        with self.assertRaises(ValueError):
            get_robot_move(board, "medium")


    def test_api_rejects_invalid_difficulty(self):
        board = create_board()

        with self.assertRaises(ValueError):
            get_robot_move(board, "impossible")


    def test_api_returns_legal_move(self):
        board = [
            ["X", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]

        move = get_robot_move(board, "medium")

        legal_moves = get_player_moves(board, ROBOT)

        self.assertIn(move, legal_moves)


    def test_api_returns_none_after_win(self):
        board = [
            ["X", "X", "X"],
            ["O", "O", ""],
            ["", "", ""]
        ]

        move = get_robot_move(board, "medium")

        self.assertIsNone(move)

    def test_both_players_cannot_win(self):
        board = [
            ["X", "X", "X"],
            ["O", "O", "O"],
            ["", "", ""]
        ]

        self.assertFalse(validate_board(board))


    def test_valid_human_win(self):
        board = [
            ["X", "X", "X"],
            ["O", "O", ""],
            ["", "", ""]
        ]

        self.assertTrue(validate_board(board))


    def test_valid_robot_win(self):
        board = [
            ["O", "O", "O"],
            ["X", "X", ""],
            ["", "", "X"]
        ]

        self.assertTrue(validate_board(board))

if __name__ == "__main__":
    unittest.main()