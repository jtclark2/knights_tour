"""
Information about various pieces that can exist on a board.
TODO: Refactor board.find_element, board.get_element, board.get_cost
"""
from enum import Enum


class Pieces(Enum):
    START = "S"
    END = "E"
    EMPTY = "."
    BARRIER = "B"
    WATER = "W"
    ROCK = "R"
    TELEPORT = "T"
    LAVA = "L"
