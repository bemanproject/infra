# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

# Default target: install and run tests.
all: install test

# Install tool:
install:
	@echo "Installing production dependencies..."
	pip3 install -r requirements.txt &> /dev/null

# Install development dependencies:
install-dev:
	@echo "Installing development dependencies..."
	pip3 install -r requirements-dev.txt &> /dev/null
	brew install autopep8 &> /dev/null
	apt-get install autopep8 -y &> /dev/null
	pip3 install autopep8

# Run tests:
test:
	@echo "Running tests..."
	python3 -m pytest tests/ -v

# Run linter:
self-lint:
	@echo "Running linter..."
	@pwd
	find . -name "*.py" | xargs autopep8 --exit-code --diff

# Run lint-fix:
self-lint-fix:
	@echo "Running linter-fix..."
	@pwd
	find . -name "*.py" | xargs autopep8 --in-place
