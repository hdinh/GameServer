CWD=$(shell pwd)
export PYTHONPATH=$(CWD)/../

all: tests pylint coverage

tests:
	python -m discover test

pylint:
	pylint tienlen test 

coverage:
	coverage run -m discover test
	coverage report -m --omit=/usr/local/lib/python2.7/dist-packages/*

