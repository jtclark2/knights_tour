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
        self.B = Board()
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
        self.B.board_grid = self.board_ground_truth
        element = self.B.get_piece(GridPos(2, 1))
        self.assertEqual(element, "S")

    @unittest.skip(
        "Seemed excessive for such a simple func..."
        "could add for increased throughness."
    )
    def test_get_element_fail(self):
        pass

    def test_get_board(self):
        """
        Grabs the actual grid, list of lists, in the board object.
        """
        self.assertEqual(self.B.board_grid, self.B.get_board())

    def test_get_width(self):
        self.B.board_grid = self.board_ground_truth[:-1]
        self.assertEqual(self.B.get_width(), 8)

    def test_get_height(self):
        self.B.board_grid = self.board_ground_truth[:-1]
        self.assertEqual(self.B.get_height(), 7)

    def test_read_board_data_verification(self):
        """
        Purpose: Verify that values are read into each position correctly
        """
        self.B.load_board("Boards/8x8_board.txt")
        for row_ground, row_read in zip(self.board_ground_truth, self.B.board_grid):
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
        for row_ground, row_read in zip(self.board_ground_truth, self.B.board_grid):
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
        self.assertEqual(len(self.B.board_grid), 8)  # column count
        self.assertEqual(len(self.B.board_grid[0]), 8)  # row count

    def test_write_board__pass(self):
        """
        Purpose: Verify that data structure is written correctly.
                 Correctly is defined as a grid, with elements in a row separated
                 by ' ', and rows separated by '\n'
        Assumptions: read_board() is also operating correctly.
                     Technically bad practice for a 'unit' test, but
                     low risk and pragmatic in this simple case.
        """

        try:
            temp_file_path = "Boards/temp_board.txt"
            self.B.write_board(self.board_ground_truth, temp_file_path)

            # Read test data
            with open("Boards/8x8_board.txt", "r", encoding="utf-8") as file:
                raw_board_ground_truth = file.read()
            with open(temp_file_path, "r", encoding="utf-8") as file:
                raw_board_written = file.read()

            self.assertEqual(raw_board_ground_truth, raw_board_written)
        finally:
            os.remove(temp_file_path)

    def test_find_element__pass_single_element(self):
        self.B.board_grid = self.board_ground_truth
        pos = self.B.find_element("S")[0]
        self.assertEqual(pos, GridPos(2, 1))

    def test_find_element__element_DNE(self):
        self.B.board_grid = self.board_ground_truth
        pos = self.B.find_element(5)
        self.assertEqual(pos, [])

    def test_reset_board(self):
        self.B.board_grid = self.board_ground_truth
        self.B.reset_board()
        self.assertEqual(self.B.get_board(), [[None] * 8] * 8)

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

        self.B.board_grid = self.board_ground_truth
        self.B.set_element(pos, value)
        self.assertEqual(self.board_ground_truth, self.B.board_grid)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BoardTester)
    unittest.TextTestRunner().run(suite)
