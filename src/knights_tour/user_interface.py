"""
Display module.
Currently contains TextUI, which just prints to stdout.

Future Improvements:
    - Add GUI
    - Formalize interface (or ABC)
"""
import copy

from src.knights_tour.grid_pos import GridPos

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
    def display_board(board, pieces=None, value_width = 2):
        """
        Displays a copy of the board.

        Note: I've chosen not to expose the underlying data structure (numpy arrays at the time of writing this).
        It makes me a little sad, since np arrays are written to be so efficient when vectorized, and this approach is
        comparatively slow since I use separate calls for every element. That said, print() is slow anyways itself,
        and I'm primarily working with smallish (~1000-2000) element boards, since they need to fit on-screen.
        This trade-off is worth it for the added encapsulation.

        Inputs:
            board: indexable 2D map
            pieces (Optional):
                Dictionary -  {piece:position}
            value_width: Largest value allowed per space. Anything large will be truncated to value_width.
                Too large a value may cause print to start wrapping.
        """

        # build a new one, so we don't just create a reference and muck up the original
        board = copy.deepcopy(board)
        if pieces is not None:
            for val, pos in pieces.items():
                board.set_element(pos, val)

        board_str = ""
        for row_index in range(board.get_height()):
            for col_index in range(board.get_width()):
                element = board.get_value(GridPos(row_index, col_index))
                board_str += '{:{width}}'.format(str(element)[:value_width], width=str(value_width+1))

            board_str = board_str[:-1]  # remove trailing ' '
            board_str = board_str + "\n"
        board_str = board_str[:-1]  # remove trailing '\n'

        print("\n" + board_str)

