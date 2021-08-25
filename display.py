"""
This file contains display implementations.
I'll start with a text-based implementation for simplicity, though I'll make them easily interchangeable.
I may build up a more flushed out display with pygame, or something, so it should be easy to swap.
"""
from board import Board
from grid_pos import GridPos


class TextDisplay:
    def __init__(self):
        pass

    @staticmethod
    def display_board(board, pieces=None):
        """
        Prints a repr of the board to the screen.

        Inputs:
            board: python list of lists, where element = board[row][col].
            pieces: Optional
                Dictionary, with display char as key, and elementDisplay pieces
                on the board, over the underlying space.
        """
        # Clean copy, so python doesn't pass the reference
        # print(("*"*50 + "\n")*5)
        # print(type(board.get_board()))
        board_copy = [row[:] for row in board]
        if pieces is not None:
            for piece in pieces:
                board_copy[pieces[piece].x][pieces[piece].y] = piece

        print("\n" + Board.board_to_str(board_copy))


display = TextDisplay()


# class Display():
#     """
#     This class is just a shell to plugin a component...basically, it's a pattern to mimick an interface in python.
#     With this, I can use the Display class, and just swap out the class in one place (more like a component).
#
#     TODO: Kind of curious if I could avoid writing out each function as well with a smart enough decorator.
#     """
#
#     def __init__(self, DisplayClass=TextDisplay, *args, **kwargs):
#         self.DisplayInstance = DisplayClass(args, kwargs)
#
#     def display_board(self, *args, **kwargs):
#         return self.DisplayClass.display_board(args, kwargs)


import unittest


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

    def test_display_board__pass(self):
        """
        Purpose: Verify that base case of board display works
        """
        import sys
        from io import StringIO

        print_buffer = StringIO()
        self.B.board = self.board_ground_truth

        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            display.display_board(self.board_ground_truth)
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
        import sys
        from io import StringIO

        print_buffer = StringIO()
        self.B.board = self.board_ground_truth
        str_board = "A" + self.str_board_ground_truth[1:]
        str_board = str_board[:34] + "K" + str_board[34 + 1 :]
        pieces = {"A": GridPos(0, 0), "K": GridPos(2, 1)}

        default_output = sys.stdout
        try:
            sys.stdout = print_buffer
            display.display_board(self.board_ground_truth, pieces)
        finally:
            sys.stdout = default_output

        # print print_buffer.getvalue()
        # print "Truth:"
        # print str_board + '\n'
        # Print automatically appends '\n', which is perfect for our usage
        self.assertEqual(print_buffer.getvalue(), "\n" + str_board + "\n")
