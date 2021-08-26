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
            # TODO: Rename to board_array (so as not to be confused with the class and module)
            self._board_grid = None
        else:
            self.load_board(board_path)

    def display_board(self, pieces=None):
        """
        Displays a copy of the board.

        Inputs:
            board: Board object
            pieces (Optional):
                Dictionary, with display char as key, and elementDisplay pieces
                on the board, over the underlying space.
        """
        board_copy = [row[:] for row in self._board_grid]
        if pieces is not None:
            for piece in pieces:
                board_copy[pieces[piece].x][pieces[piece].y] = piece

        print("\n" + Board.board_to_str(board_copy))

    def reset_board(self, value=None):
        """
        Set all spoces on the board to a specific value
        """
        for i in range(self.get_width()):
            for j in range(self.get_height()):
                self.set_element(GridPos(i, j), value)

    # TODO: Consider removing this entirely...only needs to be exposed for testing
    @property
    def grid(self):
        """
        Getter for the main data object of this class, a grid representing a board
        """
        #TODO: make sense when board was a property for backing var _board...not sure now
        return self._board_grid

    def get_value(self, pos):
        """
        Retrieve an element by index.
        Input: Index pos
        Output: Element/piece Value
        """
        return self._board_grid[pos.x][pos.y]

    def set_element(self, pos, value):
        self._board_grid[pos.x][pos.y] = value

    def find_all_elements(self, search_value):
        """
        Finds all locations of a specific element on the board.
        Inputs: The element value to search for.
        Outputs: List of element locations [y, x]
        """
        matches = []
        for row in enumerate(self._board_grid):
            for element in enumerate(row[1]):
                if element[1] == search_value:
                    matches.append(GridPos(row[0], element[0]))
        return matches

    def get_width(self):
        """
        Get the width, or number of columns of the board.
        """
        assert self._board_grid
        return len(self._board_grid[0])

    def get_height(self):
        """
        Get the height, or number of rows of the board.
        """
        assert self._board_grid
        return len(self._board_grid)

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
        self._board_grid = []
        for row in rows:
            self._board_grid.append(row.split(" "))

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

