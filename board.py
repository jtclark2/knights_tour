"""
Created by: Trevor Clark
Created on: 4/27/2017
"""

import unittest
from grid_pos import GridPos


class Board:
    """
    Manages the "board", simple object in that stores the state of the board in memory.
        - Stores the object
        - read/write capabilities
        - find/read value of pieces on various spaces in the grid
    Decoupled from any gameplay.
    """

    def __init__(self, board_path=None):
        if board_path is None:
            # TODO: Rename to board_array (so as not to be confused with the class)
            self.board = None
        else:
            self.load_board(board_path)

    def reset_board(self, value=None):
        for i in range(self.get_width()):
            for j in range(self.get_height()):
                # TODO: Why? This makes no sense...Was I in the zone, or just really tired?
                self.set_element(GridPos(i, j), value)

    def get_board(self):
        return self.board

    def get_piece(self, pos):
        """
        Retrieve an element by index.
        Input: Index pos
        Output: Element Value (assumed to be a char)
        """
        return self.board[pos.x][pos.y]

    def set_element(self, pos, value):
        self.board[pos.x][pos.y] = value

    def find_element(self, search_value):
        """
        Finds all locations of a specific element on the board.
        Inputs: The element value to search for.
        Outputs: List of element locations [y, x]
        """
        matches = []
        for row in enumerate(self.board):
            for element in enumerate(row[1]):
                if element[1] == search_value:
                    matches.append(GridPos(row[0], element[0]))
        return matches

    def get_width(self):
        """
        Calculate and return the width, or number of columns.
        """
        assert self.board
        return len(self.board[0])

    def get_height(self):
        """
        Calculate and return the height, or number of rows.
        """
        assert self.board
        return len(self.board)

    def load_board(self, file_path):
        """
        Reads the board from a text file, parsing and loading into memory
        TODO: should probably just use 2D numpy array
        File Format: ' ' delimits elements in a row, and '\n' delimits between rows
        Assumptions/Limitations: Does not handle/pad non-rectangular boards.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            board_str = file.read()

        rows = board_str.split("\n")
        self.board = []
        for row in rows:
            self.board.append(row.split(" "))

    def write_board(self, board=None, write_path="./temp_board"):
        """
        Writes a copy of the boards current state as a txt file.

        Inputs:
            board: python list of lists, where element = board[row][col].

            write_path: path that file will be written to
                File Format: grid delimited by ' ' between elements and '\n' between rows.

        Outputs: None

        """

        # construct string for file write
        # TODO: Consider implementing as __repr__
        board_str = self.board_to_str(board)

        with open(write_path, "w", encoding="utf-8") as file:
            file.write(board_str)

    @staticmethod
    def board_to_str(board):
        """
        Purpose: Take the 2D board and turn it into a str
        Inputs: board
        Outputs: str representation of board (matches file and convenient display)

        Note: While board is intrinsic to this class, the str repr is not. It
            may require alteration to show pieces overlaid on the board, so we
            allow board as an explicit input arg, with self.board as the
            default.
        """
        board_str = ""
        for row in board:
            for element in row:
                board_str = board_str + ("%s " % element)
            board_str = board_str[:-1]  # remove trailing ' '
            board_str = board_str + "\n"
        board_str = board_str[:-1]  # remove trailing '\n'
        return board_str


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
        self.B.board = self.board_ground_truth
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
        self.assertEqual(self.B.board, self.B.get_board())

    def test_get_width(self):
        self.B.board = self.board_ground_truth[:-1]
        self.assertEqual(self.B.get_width(), 8)

    def test_get_height(self):
        self.B.board = self.board_ground_truth[:-1]
        self.assertEqual(self.B.get_height(), 7)

    def test_read_board_data_verification(self):
        """
        Purpose: Verify that values are read into each position correctly
        """
        self.B.load_board("Boards/8x8_board.txt")
        for row_ground, row_read in zip(self.board_ground_truth, self.B.board):
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
        for row_ground, row_read in zip(self.board_ground_truth, self.B.board):
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
        self.assertEqual(len(self.B.board), 8)  # column count
        self.assertEqual(len(self.B.board[0]), 8)  # row count

    def test_write_board__pass(self):
        """
        Purpose: Verify that data structure is written correctly.
                 Correctly is defined as a grid, with elements in a row separated
                 by ' ', and rows separated by '\n'
        Assumptions: read_board() is also operating correctly.
                     Technically bad practice for a 'unit' test, but
                     low risk and pragmatic in this simple case.
        """

        self.B.write_board(self.board_ground_truth)

        # Read test data
        with open("Boards/8x8_board.txt", "r", encoding="utf-8") as file:
            raw_board_ground_truth = file.read()
        with open("temp_board", "r", encoding="utf-8") as file:
            raw_board_written = file.read()

        self.assertEqual(raw_board_ground_truth, raw_board_written)

    def test_find_element__pass_single_element(self):
        self.B.board = self.board_ground_truth
        pos = self.B.find_element("S")[0]
        self.assertEqual(pos, GridPos(2, 1))

    def test_find_element__element_DNE(self):
        self.B.board = self.board_ground_truth
        pos = self.B.find_element(5)
        self.assertEqual(pos, [])

    def test_reset_board(self):
        self.B.board = self.board_ground_truth
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

        self.B.board = self.board_ground_truth
        self.B.set_element(pos, value)
        self.assertEqual(self.board_ground_truth, self.B.board)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(BoardTester)
    unittest.TextTestRunner().run(suite)
