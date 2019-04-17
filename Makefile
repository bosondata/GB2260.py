PYTHON := python
PYTEST := py.test
TOX := tox

.PHONY: all build test test-all clean

all: build

build: gb2260_v2/data/__init__.py
	$(PYTHON) setup.py sdist bdist_wheel

test: gb2260_v2/data/__init__.py
	$(PYTEST)

test-all: gb2260_v2/data/__init__.py
	$(TOX)

clean:
	rm -rf dist build *.egg-info gb2260_v2/data/

gb2260_v2/data/__init__.py: data/revisions.json
	$(PYTHON) generate.py $?
