install:
	pip install --upgrade pip
# 	pip install -r requirements.txt
	pip install black
	pip install pylint
	pip install pytest

format:
	black *.py

lint:
	pylint --disable=R,C *.py

test:
    # TODO: run via pytest commands (currently, the tests are also the entry point)
	python board.py
	python knight.py

save_requirements:
	pip freeze > requirements.txt
# 	conda env export > environment.yml

all: install format lint test build_env