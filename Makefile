.PHONY: help setup dev test lint fmt docker/build docker/run streamlit clean

# Default target
help:
	@echo "Available commands:"
	@echo "  setup       - Install dependencies and setup development environment"
	@echo "  dev         - Run development server (FastAPI)"
	@echo "  streamlit   - Run Streamlit web interface"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting checks"
	@echo "  fmt         - Format code"
	@echo "  docker/build - Build Docker image"
	@echo "  docker/run   - Run Docker container"
	@echo "  clean       - Clean up temporary files"

# Setup development environment
setup:
	python3 -m pip install --upgrade pip
	python3 -m pip install -e .[dev]

# Run development server
dev:
	python3 -m src.app

# Run Streamlit web interface
streamlit:
	streamlit run streamlit_app.py

# Run tests
test:
	pytest -v --cov=src --cov-report=term-missing

# Lint code
lint:
	ruff check src tests
	mypy src
	black --check src tests

# Format code
fmt:
	ruff check --fix src tests
	black src tests

# Build Docker image
docker/build:
	docker build -t workflow-api:latest .

# Run Docker container
docker/run:
	docker run -p 8000:8000 --env-file .env workflow-api:latest

# Clean up
clean:
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/
