"""
This is a demonstration of the solutions to the 5 prompt problems.
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

# import termcolor
# from termcolor import colored
# print(colored('hello', 'red'), colored('world', 'green'))
board_dir = "../Boards"
board_8x8 = board_dir + "/8x8_board.txt"
board_32x32 = board_dir + "/32x32_board.txt"
game_engine = GameEngine(Board(board_8x8))


print("Run from 'knightboard/src/'")
# Prompt problem #1:
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
pieces = {f"{val}":pos for val,pos in enumerate(positions)}
game_engine.board.display_board(pieces=pieces, value_width=1)
valid = game_engine.validate_pos_sequence(positions)
print(f"The first 5 moves valid (expect: True)? {valid}")

#Invalid move,
positions.append(GridPos(0, 7)) #Invalid
pieces = {f"{val}":pos for val,pos in enumerate(positions)}
game_engine.board.display_board(pieces=pieces, value_width=1)
valid = game_engine.validate_pos_sequence(positions)
print(f"The sixth move is not (expect: False)? {valid}")

# Prompt problem #2 & #3:
print('\n::::::::::Prompt 2 & 3::::::::::')
squire = Knight(GameEngine(Board(board_8x8)))

print("Loaded map:")
squire.game_mechanics.board.display_board(value_width=1)
print("Solution:")
squire.plan_path()
path = squire.reconstruct_path()
squire.display_path_as_grid(path)
squire.display_path_as_list(path)

# Prompt problem #2 & #3:
print('\n::::::::::Prompt 4::::::::::')
# TODO: not reloading boards correctly...honestly, this whole thing is a mess, and I just need to use numpy instead
#   of the board class

print("World map:")
knight = Knight(GameEngine(Board(board_32x32)), start_pos=GridPos(2, 2), end_pos=GridPos(30, 30))
knight.game_mechanics.board.display_board(value_width=2)

print("Solution:")
knight.plan_path()
path = knight.reconstruct_path()
knight.display_path_as_grid(path)
knight.display_path_as_list(path)