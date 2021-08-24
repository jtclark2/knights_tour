install:
	pip3 install --upgrade pip
	pip install -r requirements.txt

format:
	black *.py

lint:
	pylint --disable=R,C *.py

test:
	pytest -v *.py

all: install format test lint
