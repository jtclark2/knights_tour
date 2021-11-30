# Status
[![Python application](https://github.com/jtclark2/knights_tour/actions/workflows/python-app.yml/badge.svg)](https://github.com/jtclark2/knights_tour/actions/workflows/python-app.yml)

# KnightBoard Problem Statement
This repo addressing a series of increasingly complex maze/pathfinding problems state in the prompt [KnightBoard.pdf](https://github.com/jtclark2/knights_tour/blob/master/Reference/KnightBoard.pdf). 
- (Part 1) The solutions start with implementation of simple code to build a chess board and move a knight around on it. 
- (Parts 2-4) Optimal path planning algorithms are built with increasingly complex rules and obstacles being added to the world.
  - Features: Dynamic Programming
- (Part 5) Hamiltonian path problem in the form of the knights tour
  - Faetures: Heuristic search
  - This problem is NP-complete, so we're not solving it perfectly, but using heuristics to explore a variety of partial solutions.

* I've forgetten the original source of this prompt...If anyone knows, please share with me, so I can properly credit the author.

# Setup:
Linux: Create env, and run "make all"
Other OS: Take a look at the makefile. It requires python and a few packages listed in requirements.txt

# Run:
Linux: "make run"
Other: From the root of this project run "python src/main.py"

## Command Line arguments
If no arguments are added, it will run all prompts. This is a great way to the whole project in action, though 
you will get a wall of text (the UI is text-based) so you'll have to scroll up.

# Author: 
Trevor Clark

# Setup
Create new env, and run `make all`. This will run the install scripts and a bunch of other checks.


# Future Improvements:
There are Todo's noted throughout the code, but nothing critical. Just tweaks for fun, that I might add
if this project grew into a real game.
