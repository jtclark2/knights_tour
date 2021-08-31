"""
This is a demonstration of the solutions to the 5 prompt problems.
Note that my display is in the "spirit" of the prompt. The literal interpretation gives the option to
print the world after each step, and that becomes verbose and confusing. Instead, I print the the path of the journey.
Each number is the total cost to reach that point (most steps cost=1, so it's almost like numbering the steps).

To experiment more, the specific solvers can be called:
    Problem

Level 1: Call Knight().validate_pos_sequence(node_sequence)

Level 2, 3 & 4: These are the same problem, just in increasing complexity.
    Call Knight().plan_shortest_path() to map the space, followed by Knight().reconstruct_path()
    to build the path.

Level 5:
    I built this...the display was messy, but did I forget to commit it?
"""
import sys

from knights_tour.knight import Knight
from knights_tour.gameengine import GameEngine
from knights_tour.grid_pos import GridPos
from knights_tour.board import Board
from knights_tour.user_interface import UI
from knights_tour.heuristics import LongestPathSearchHeuristics as Heuristics

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
board_32x32_mod = board_dir + "/32x32_board_mod.txt"

try:
    game_engine = GameEngine(Board(board_8x8))
except FileNotFoundError as err:
    raise FileNotFoundError("Directory of Boards may be incorrect. Either use 'make run', run from '/src', or"
                            "edit the board_dir in 'main.py'.") from err

def prompt1():
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

def prompt2():
    prompt3()

def prompt3():
    print('\n::::::::::Prompt 2 & 3::::::::::')
    squire = Knight(GameEngine(Board(board_8x8)))

    print("Loaded map:")
    UI.display_board(squire.game_engine.board, value_width=1)
    print("Solution:")
    squire.plan_shortest_path()
    path = squire.reconstruct_path()
    UI.display_path_as_grid(squire.game_engine.board, path, squire.cost_map)
    UI.display_path_as_list(path, squire.cost_map)

def prompt4():
    print('\n::::::::::Prompt 4::::::::::')
    print("World map:")
    knight = Knight(GameEngine(Board(board_32x32_mod)), start_pos=GridPos(2, 2), end_pos=GridPos(30, 30))
    UI.display_board(knight.game_engine.board, value_width=2)

    print("Solution:")
    knight.plan_shortest_path()
    path = knight.reconstruct_path()
    UI.display_path_as_list(path, knight.cost_map)
    UI.display_path_as_grid(knight.game_engine.board, path, knight.cost_map)
    print("The map above shows the path solved. Various spaces on the board have different special properties, such as"
          "lava (costs 5 to land on) and teleports, which connection 2 distance spaces at a cost of 1. To see the"
          "map this path was built on, scroll up.")

def prompt5():
    print('\n::::::::::Prompt 5 (knights tour - hamiltonian path problem)::::::::::')
    print("World map:")
    squire = Knight(GameEngine(Board(board_8x8)))
    squire.find_longest_path_entry(heuristic=Heuristics().dense_search_heuristic)
    squire.print_longest_path()

    knight = Knight(GameEngine(Board(board_32x32_mod)), start_pos=GridPos(2, 2), end_pos=GridPos(30, 30))

    ### including these just to play with. It's fun to see how each react
    heuristic = Heuristics().identity_heuristic
    # heuristic = Heuristics().dense_search_heuristic
    # heuristic = Heuristics().sparse_search_heuristic
    # heuristic = Heuristics().random_search_heuristic

    knight.find_longest_path_entry(time_allowed = 10,
                                   heuristic = heuristic)
    knight.print_longest_path()
    print("\n\n\nThis problem reduces to the hamiltonian path problem, which is NP-complete, so we don't solve it. "
          "\nHowever, we can use some heuristics to improve on brute force in the simpler cases. We can also get "
          "\nsome high scores, even if we can't guarantee highest. These solutions don't force the endpoint to match."
          "\nIn order to ensure that, you need to run plan_shortest_path(), and then continually pop entries off the end of the"
          "path, until a solution is found. But it's a lot less interesting than this!")

if __name__ == '__main__':
    print("*"*50)
    if(len(sys.argv) == 2):
        prompt = int(sys.argv[1])
        print(prompt)
    else:
        prompt = None

    if prompt is None or prompt == 0:
        prompt1()
        prompt3() # 2 and 3 are redundant
        prompt4()
        prompt5()

    if prompt == 1:
        prompt1()

    if prompt == 2:
        prompt2()

    if prompt == 3:
        prompt3()

    if prompt == 4:
        prompt4()

    if prompt == 5:
        prompt5()