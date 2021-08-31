install:
	pip3 install --upgrade pip
	pip install -r requirements.txt

format:
	black *.py

# Disable can be applied here or in comments in specific chunks of code. Disables certain linting errors/warnings
# Decided not disable the fixme (TODO), this isn't production, so don't want don't want my notes causing build failures
lint:
	pylint --disable=R,C,fixme,import-error src/knights_tour/*.py
	pylint --disable=R,C,fixme,protected-access,import-error tests/*.py

# test and coverage report
# "python -m" creates a module from setup.py, allowing the package imports to work
# -v adjust verbosity
# --cov=. provides a coverage report for everything within the current directory (the one the makefile is in)
# Test/*.py specifies which files to test
# TODO: I might not understand --cov=.
test:
	python -m pytest -v --cov=. tests/*.py

all: install format test lint


run:
	python src/main.py
