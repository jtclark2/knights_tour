# 3rd party
import sys
from io import StringIO
import unittest

# Resources
from src.knights_tour.gameengine import GameEngine
from src.knights_tour.grid_pos import GridPos
from src.knights_tour.board import Board
from src.knights_tour.pieces import Pieces

# Test target
from src.knights_tour import user_interface



class BoardTester(unittest.TestCase):
    def setUp(self):
        """
        Init board for each test.
        """

        self.board = Board("Boards/8x8_board.txt")

        # Using trivial var names for readability
        S = Pieces.START.value
        E = Pieces.END.value
        _ = Pieces.EMPTY.value
        self.board_ground_truth = [
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, S, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, E, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
            [_, _, _, _, _, _, _, _],
        ]

        self.str_board_ground_truth = (
            f"{_} {_} {_} {_} {_} {_} {_} {_}\n"
            f"{_} {_} {_} {_} {_} {_} {_} {_}\n"
            f"{_} {S} {_} {_} {_} {_} {_} {_}\n"
            f"{_} {_} {_} {_} {_} {_} {_} {_}\n"
            f"{_} {_} {_} {_} {_} {E} {_} {_}\n"
            f"{_} {_} {_} {_} {_} {_} {_} {_}\n"
            f"{_} {_} {_} {_} {_} {_} {_} {_}\n"
            f"{_} {_} {_} {_} {_} {_} {_} {_}"
        )

    def test_display_board__pass(self):
        """
        Purpose: Verify that base case of board display works
        """
        print_buffer = StringIO()
        self.board._board_grid = self.board_ground_truth

        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            user_interface.TextUI.display_board(self.board, value_width=1)
        finally:
            sys.stdout = default_output

        # Print automatically appends '\n', which is perfect for our usage
        self.assertEqual(
            print_buffer.getvalue(), "\n" + self.str_board_ground_truth + "\n"
        )

    def test_display_board__input_pieces(self):
        """
        Purpose: Verify board display works when passing in chars.
        """
        print_buffer = StringIO()
        self.board._board_grid = self.board_ground_truth
        str_board = Pieces.ROCK.value + self.str_board_ground_truth[1:]
        str_board = str_board[:34] + Pieces.LAVA.value + str_board[34 + 1 :]
        pieces = {GridPos(0, 0):Pieces.ROCK.value, GridPos(2, 1):Pieces.LAVA.value}

        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            user_interface.TextUI.display_board(self.board, pieces, value_width=1)
        finally:
            sys.stdout = default_output

        print(print_buffer.getvalue())
        print("Truth:")
        print(str_board + '\n')
        self.assertEqual(print_buffer.getvalue(), "\n" + str_board + "\n")
