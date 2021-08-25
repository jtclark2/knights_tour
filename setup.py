#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="KnightsTour",
    version="1.0.0",
    author_email="jtclark2@gmail.com",
    author="Trevor Clark",
    url="https://github.com/jtclark2/knights_tour",
    # a bit tedious to maintain modules, just reference the whole package
    # py_modules=['knight', 'board', 'grid_pos', 'pieces'],
    packages=find_packages(where="src"),  # ['knights_tour'],
    package_dir={"": "src"},
    description="Play with pathfinding with a piece the uses the L-shaped moves of a knight.",
)
