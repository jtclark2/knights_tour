"""
This is become circular for the text based case. I want the board object to standardize and own
text-based representation (for read/write/display), so the display class needs to use the board's representation.
However, the board needs the display class (dependency inversion) to properly interchangeable.

If I decide to pick this up again, I may separate the on-screen display representation from the file read/write
representation, so that they are not coupled, and the circular dependency goes away. This introduces a small,
but acceptable chance that the text based display string representation diverges from the representation saved to file.
"""



from .board import Board

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
    def display_board(grid, pieces=None):
        """
        Displays a copy of the board.

        Inputs:
            board: Board object
            pieces (Optional):
                Dictionary, with display char as key, and elementDisplay pieces
                on the board, over the underlying space.
        """
        board_copy = [row[:] for row in grid]
        if pieces is not None:
            for piece in pieces:
                board_copy[pieces[piece].x][pieces[piece].y] = piece

        #TODO: I put an extended note as the beginning of this file...get rid of dependency on "board_to_str"
        print("\n" + Board.board_to_str(board_copy))

UI = TextUI
