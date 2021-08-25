"""
Created by: Trevor Clark
Created on: 4/27/2017
"""
from .grid_pos import GridPos


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
        """
        Set all spoces on the board to a specific value
        """
        for i in range(self.get_width()):
            for j in range(self.get_height()):
                self.set_element(GridPos(i, j), value)

    def get_board(self):
        #TODO: make sense when board was a property for backing var _board...not sure now
        return self.board

    def get_piece(self, pos):
        """
        Retrieve an element by index.
        Input: Index pos
        Output: Element/piece Value
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
        Get the width, or number of columns of the board.
        """
        assert self.board
        return len(self.board[0])

    def get_height(self):
        """
        Get the height, or number of rows of the board.
        """
        assert self.board
        return len(self.board)

    def load_board(self, file_path):
        """
        TODO: should probably just use 2D numpy array
        Reads the board from a text file, parsing and loading into memory
        File Format: ' ' delimits elements in a row, and '\n' delimits between rows
        Assumptions/Limitations: All boards must be rectangular, though not rectangular problems can be formatted
        by adding Barriers ("B") to the unavailable space.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            board_str = file.read()

        rows = board_str.split("\n")
        self.board = []
        for row in rows:
            self.board.append(row.split(" "))

    def write_board(self, board=None, write_path="Boards/temp_board.txt"):
        """
        Writes a copy of the boards current state as a txt file.
        Inputs:
            board: python list of lists, where element = board[row][col].

            write_path: path that file will be written to
                File Format: grid delimited by ' ' between elements and '\n' between rows.

        Outputs: None

        Side Effects: Writes the board
        """
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

