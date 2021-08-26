"""
Display module.
Currently contains TextUI, which just prints to stdout.

Future Improvements:
    - Add GUI
    - Formalize interface (or ABC)
"""


# TODO: Formalize as an interface/abstract base class
# class UI:
#     def __init__(self):
#         raise NotImplementedError
#
#     @staticmethod
#     def display_board(board, pieces=None):
#         raise NotImplementedError

class TextUI:
    def __init__(self):
        pass

    @staticmethod
    def display_board(grid, pieces=None, value_width = 2):
        """
        Displays a copy of the board.

        Inputs:
            board: indexable 2D map
            pieces (Optional):
                Dictionary -  {piece:position}
            value_width: Largest value allowed per space. Anything large will be truncated to value_width.
                Too large a value may cause print to start wrapping.
        """
        board_copy = [row[:] for row in grid]
        if pieces is not None:
            for piece in pieces:
                board_copy[pieces[piece].x][pieces[piece].y] = piece

        board_str = ""
        for row in board_copy:
            for element in row:
                board_str += '{:{width}}'.format(str(element)[:value_width], width=str(value_width+1))

            board_str = board_str[:-1]  # remove trailing ' '
            board_str = board_str + "\n"
        board_str = board_str[:-1]  # remove trailing '\n'

        print("\n" + board_str)

