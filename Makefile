install:
	pip3 install --upgrade pip
	pip install -r requirements.txt

format:
	black *.py

# Decided not disable the fixme (TODO), this isn't production, so don't want don't want my notes causing build failures
lint:
	pylint --disable=R,C,fixme *.py

test:
	pytest -v *.py

all: install format test lint
