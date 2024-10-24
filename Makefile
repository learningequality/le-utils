.PHONY: clean clean-test clean-pyc clean-build test release build-labels

clean: clean-build clean-pyc clean-test

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

test:
	pytest -s

build:
	pip install -e .
	python scripts/generate_from_specs.py

dist: clean build
	python setup.py sdist

release: dist
	twine upload dist/*.tar.gz

release-npm: clean build
	cd js && npm publish
