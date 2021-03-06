"""
Purpose:
Encapsulate the operations of a board, which manages placement/navigation of objects in positions.

Assumptions:
    a) Board is rectangular, though non-rectangular shapes can be calculated by populating the Barriers.

Created by: Trevor Clark

Tehnical note: Board is a wrapper for 2D grid. Originally, numpy seemed like the obvious choice, but I ended up
using list(list()) instead, despite the drawbacks to speed. Reasons include:
    1) Easily support str, num, and None value types
    2) pass around coodinate position objects, rather than x and y values (or a 1D array of 2 values)
    3) No need to install numpy
    4) My application isn't vectorized (and the algorithm isn't really well-suited for that). That means I wouldn't
    get the performance gains anways, since I'm accessing random elements, rather than passing entire vectors/arrays.
"""

from .grid_pos import GridPos


class Board:
    def __init__(self, file_path):
        """
        Reads the board from a text file, parsing and loading into memory
        File Format: ' ' delimits elements in a row, and '\n' delimits between rows
        Assumptions/Limitations: All boards must be rectangular, though not rectangular problems can be formatted
        by adding Barriers to the unavailable space.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            board_str = file.read()

        rows = board_str.split("\n")
        self._board_grid = []
        for row in rows:
            self._board_grid.append(row.split(" "))

    def reset_board(self, value=None):
        """
        Set all elements on the board to a specific value
        """
        for i in range(self.get_width()):
            for j in range(self.get_height()):
                self.set_element(GridPos(i, j), value)

    def get_value(self, pos):
        """
        Retrieve an element by index.
        Input: Index pos
        Output: Element/piece Value
        """
        try:
            return self._board_grid[pos.x][pos.y]
        except IndexError:
            print(f"Index out of range. Board size: {self.get_width(), self.get_height()}\tpos: {pos}")
            raise
        except AttributeError as err:
            raise AttributeError(f"get_value failed because of data type. Instead of GridPos, it tried to get -> "
                                 f"{type(pos)}: {pos}") from err



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
