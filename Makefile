all: check

check: black flake8

black:
	black src/

flake8:
	flake8 --ignore E501 src/
