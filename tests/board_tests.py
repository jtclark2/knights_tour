import unittest
import os

# local imports
from src.knights_tour.grid_pos import GridPos

# test target
from src.knights_tour.board import Board


class BoardTester(unittest.TestCase):
    def setUp(self):
        """
        Init board for each test.
        """
        self.B = Board("Boards/8x8_board.txt")
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

    def test_get_element_pass(self):
        self.B._board_grid = self.board_ground_truth
        element = self.B.get_value(GridPos(2, 1))
        self.assertEqual(element, "S")

    def test_get_board(self):
        """
        Grabs the actual grid, list of lists, in the board object.
        """
        self.assertEqual(self.B._board_grid, self.B.grid)

    def test_get_width(self):
        self.B._board_grid = self.board_ground_truth[:-1]
        self.assertEqual(self.B.get_width(), 8)

    def test_get_height(self):
        self.B._board_grid = self.board_ground_truth[:-1]
        self.assertEqual(self.B.get_height(), 7)

    def test_read_board_data_verification(self):
        """
        Purpose: Verify that values are read into each position correctly
        """
        self.B.load_board("Boards/8x8_board.txt")
        for row_ground, row_read in zip(self.board_ground_truth, self.B._board_grid):
            for element_ground, element_read in zip(row_ground, row_read):
                self.assertEqual(element_ground, element_read)

    def test_read_board_data_verification_fail(self):
        """
        Purpose: Verify that values are read into each position correctly.
        Note: A negative case on a literal match is probably overkill, but
              quick enough to implement, so...
        """

        self.board_ground_truth[5][3] = "S"  # Overwrite the correct data

        match = True
        self.B.load_board("Boards/8x8_board.txt")
        for row_ground, row_read in zip(self.board_ground_truth, self.B._board_grid):
            for element_ground, element_read in zip(row_ground, row_read):
                if element_ground != element_read:
                    match = False
        self.assertFalse(match)

    def test_read_board__dimension_match(self):
        """
        Purpose: Verify that the board dimensions match the .txt file
        Assumptions: 8x8_board.txt is well formatted, and represents an 8x8
        """
        self.B.load_board("Boards/8x8_board.txt")
        self.assertEqual(len(self.B._board_grid), 8)  # column count
        self.assertEqual(len(self.B._board_grid[0]), 8)  # row count

    def test_find_element__pass_single_element(self):
        self.B._board_grid = self.board_ground_truth
        pos = self.B.find_all_elements("S")[0]
        self.assertEqual(pos, GridPos(2, 1))

    def test_find_element__element_DNE(self):
        self.B._board_grid = self.board_ground_truth
        pos = self.B.find_all_elements(5)
        self.assertEqual(pos, [])

    def test_reset_board(self):
        self.B._board_grid = self.board_ground_truth
        self.B.reset_board()
        self.assertEqual(self.B.grid, [[None] * 8] * 8)

    def test_set_element(self):
        pos = GridPos(2, 7)
        value = 5

        self.board_ground_truth = [
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", "S", ".", ".", ".", ".", ".", 5],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", "E", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
        ]

        self.B._board_grid = self.board_ground_truth
        self.B.set_element(pos, value)
        self.assertEqual(self.board_ground_truth, self.B._board_grid)
