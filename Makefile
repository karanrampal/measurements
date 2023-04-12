SHELL := /bin/bash
CONDAENV := environment.yml
REQ := requirements.txt

# Docker
PROJECT := airesearch-1409
LOCATION := europe-west4
REGISTRY := api-store
IMG := measurement:latest

install: $(CONDAENV)
	conda env create -f $(CONDAENV)

install_ci: $(REQ)
	pip install --upgrade pip &&\
		pip install -r $(REQ)

build:
	python -m build

test:
	pytest -vv --cov --disable-warnings --cov-report=xml

format:
	black src tests
	isort src tests
	mypy src tests

lint:
	pylint -j 4 src tests

docker_bp: Dockerfile
	docker build -f Dockerfile -t $(LOCATION)-docker.pkg.dev/$(PROJECT)/$(REGISTRY)/$(IMG) ./
	docker push $(LOCATION)-docker.pkg.dev/$(PROJECT)/$(REGISTRY)/$(IMG)

clean:
	rm -r coverage.xml .coverage .mypy_cache .pytest_cache dist src/*.egg-info
	find . -name "__pycache__" -exec rm -r {} +

all: install lint test

.PHONY: lint format clean all