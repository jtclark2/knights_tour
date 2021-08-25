"""
This file contains display implementations.
I'll start with a text-based implementation for simplicity, though I'll make them easily interchangeable.
I may build up a more flushed out display with pygame, or something, so it should be easy to swap.
"""
from .board import Board

class TextUI:
    def __init__(self):
        pass

    @staticmethod
    def display_board(board, pieces=None):
        """
        Displays a copy of the board.

        Inputs:
            board: Board object
            pieces (Optional):
                Dictionary, with display char as key, and elementDisplay pieces
                on the board, over the underlying space.
        """
        board_copy = [row[:] for row in board]
        if pieces is not None:
            for piece in pieces:
                board_copy[pieces[piece].x][pieces[piece].y] = piece

        print("\n" + Board.board_to_str(board_copy))

UI = TextUI
