# 3rd party
import sys
from io import StringIO
import unittest

# Resources
from src.knights_tour.gameengine import GameEngine
from src.knights_tour.grid_pos import GridPos
from src.knights_tour.board import Board

# Test target
from src.knights_tour import user_interface



class BoardTester(unittest.TestCase):
    def setUp(self):
        """
        Init board for each test.
        """

        import os
        print("*"*1000)
        print(os.path)

        self.mech = GameEngine(Board("Boards/8x8_board.txt"))
        self.board_ground_truth = [
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", "S", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", "E", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
        ]

        self.str_board_ground_truth = (
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". S . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . E . .\n"
            ". . . . . . . .\n"
            ". . . . . . . .\n"
            ". . . . . . . ."
        )

    def test_display_board__pass(self):
        """
        Purpose: Verify that base case of board display works
        """
        print_buffer = StringIO()
        self.mech._board_grid = self.board_ground_truth

        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            user_interface.TextUI.display_board(self.board_ground_truth, value_width=1)
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
        self.mech._board_grid = self.board_ground_truth
        str_board = "A" + self.str_board_ground_truth[1:]
        str_board = str_board[:34] + "K" + str_board[34 + 1 :]
        pieces = {"A": GridPos(0, 0), "K": GridPos(2, 1)}

        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            user_interface.TextUI.display_board(self.board_ground_truth, pieces, value_width=1)
        finally:
            sys.stdout = default_output

        print(print_buffer.getvalue())
        print("Truth:")
        print(str_board + '\n')
        self.assertEqual(print_buffer.getvalue(), "\n" + str_board + "\n")
