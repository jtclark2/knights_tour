"""
This is a demonstration of the solutions to the 5 prompt problems.
To experiment more, the specific solvers can be called:
    Problem

Level 1: Call Knight().validate_pos_sequence(node_sequence, rich_print)

Level 2, 3 & 4: These are the same problem, just in increasing complexity.
    Call Knight().plan_path() to map the space, followed by Knight().reconstruct_path()
    to build the path.

Level 5:
    I build this...did I forget to commit it?
"""

from knights_tour.knight import Knight
from knights_tour.board import Board
from knights_tour.grid_pos import GridPos

# import termcolor
# from termcolor import colored
# print(colored('hello', 'red'), colored('world', 'green'))
board_dir = "../Boards"
board_8x8 = board_dir + "/8x8_board.txt"
board_32x32 = board_dir + "/32x32_board.txt"
my_knight = Knight(Board(board_8x8))

positions = [
    GridPos(0, 0),
    GridPos(2, 1),
    GridPos(4, 0),
    GridPos(3, 2),
    GridPos(4, 4),
    GridPos(6, 5),
    GridPos(0, 0), #Invalid
]
print("Run from 'knightboard/src/'")
# Prompt problem #1:
# Turn on updates with richprint (though printing every single step is noisy, so I just map it at the end)
print('\n::::::::::Prompt 1::::::::::')

valid = my_knight.validate_pos_sequence(positions[:-1])
print(f"Are first 5 moves valid (expect: True)? {valid}")
valid = my_knight.validate_pos_sequence(positions)
print(f"Are all 6 moves valid (expect: False)? {valid}")

# Display (not strictly part of this problem, but added for readability)
my_knight.board.reset_board(".")
pieces = {f"{val}":pos for val,pos in enumerate(positions)}
my_knight.board.display_board(pieces=pieces, value_width=1)

# Prompt problem #2 & #3:
print('\n::::::::::Prompt 2 & 3::::::::::')
my_knight.board.load_board(board_8x8)
print("Loaded map:")
my_knight.display_current_map()
print("Solution:")
my_knight.plan_path()
path = my_knight.reconstruct_path()
my_knight.display_path_as_grid(path)
my_knight.display_path_as_list(path)

# Prompt problem #2 & #3:
print('\n::::::::::Prompt 4::::::::::')
# TODO: not reloading boards correctly...honestly, this whole thing is a mess, and I just need to use numpy instead
#   of the board class
# my_knight.board.load_board(board_32x32)
# print("Loaded map:")
# my_knight.display_current_map()
# print("Solution:")
# my_knight.plan_path()
# path = my_knight.reconstruct_path()
# my_knight.display_path_as_grid(path)
# my_knight.display_path_as_list(path)