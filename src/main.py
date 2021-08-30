"""
This is a demonstration of the solutions to the 5 prompt problems.
Note that my display is in the "spirit" of the prompt. The literal interpretation gives the option to
print the world after each step, and that becomes verbose and confusing. Instead, I print the the path of the journey.
Each number is the total cost to reach that point (most steps cost=1, so it's almost like numbering the steps).

To experiment more, the specific solvers can be called:
    Problem

Level 1: Call Knight().validate_pos_sequence(node_sequence)

Level 2, 3 & 4: These are the same problem, just in increasing complexity.
    Call Knight().plan_path() to map the space, followed by Knight().reconstruct_path()
    to build the path.

Level 5:
    I built this...the display was messy, but did I forget to commit it?
"""

from knights_tour.knight import Knight
from knights_tour.gameengine import GameEngine
from knights_tour.grid_pos import GridPos
from knights_tour.board import Board
from knights_tour.user_interface import UI

# import termcolor
# from termcolor import colored
# print(colored('hello', 'red'), colored('world', 'green'))
from pathlib import Path


import os
cwd = os.getcwd()
split = os.path.split(cwd)
parent_dir = split[-1]

if(parent_dir == "src"):
    board_dir = "../Boards"
else:
    board_dir = "Boards"    # Relative path if running from the make file (since absolute path unknown)

board_8x8 = board_dir + "/8x8_board.txt"
board_32x32 = board_dir + "/32x32_board.txt"

try:
    game_engine = GameEngine(Board(board_8x8))
except FileNotFoundError as err:
    raise FileNotFoundError("Directory of Boards may be incorrect. Either use 'make run', run from '/src', or"
                            "edit the board_dir in 'main.py'.") from err

print("Run from 'knightboard/src/'")

print('\n::::::::::Prompt 1::::::::::')
# Ensure board is empty to start
game_engine.board.reset_board(".")

# Valid moves
positions = [
    GridPos(0, 0),
    GridPos(2, 1),
    GridPos(4, 0),
    GridPos(3, 2),
    GridPos(4, 4),
    GridPos(6, 5)
]
pieces = {pos: f"{val}" for val,pos in enumerate(positions)}
UI.display_board(game_engine.board, pieces=pieces, value_width=1)
valid = game_engine.validate_pos_sequence(positions)
print(f"The first 5 moves valid (expect: True)? {valid}")

# Invalid move
positions.append(GridPos(0, 7)) # Invalid
pieces = {pos:f"{val}" for val,pos in enumerate(positions)}
UI.display_board(game_engine.board, pieces=pieces, value_width=1)
valid = game_engine.validate_pos_sequence(positions)
print(f"The sixth move is not (expect: False)? {valid}")


print('\n::::::::::Prompt 2 & 3::::::::::')
squire = Knight(GameEngine(Board(board_8x8)))

print("Loaded map:")
UI.display_board(squire.game_engine.board, value_width=1)
print("Solution:")
squire.plan_path()
path = squire.reconstruct_path()
UI.display_path_as_grid(squire.game_engine.board, path, squire.cost_map)
UI.display_path_as_list(path, squire.cost_map)


print('\n::::::::::Prompt 4::::::::::')
print("World map:")
knight = Knight(GameEngine(Board(board_32x32)), start_pos=GridPos(2, 2), end_pos=GridPos(30, 30))

print("Solution:")
knight.plan_path()
path = knight.reconstruct_path()
UI.display_path_as_list(path, knight.cost_map)
UI.display_path_as_grid(knight.game_engine.board, path, knight.cost_map)


print('Scroll up to see solutions to all the prompts.')