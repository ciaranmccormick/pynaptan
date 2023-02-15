default:
  @just --list

# Run linting and mypy checks
lint:
	poetry run flake8 pynaptan
	poetry run mypy pynaptan tests/**/*.py

# Run unit tests
test:
	poetry run pytest tests/

# Check packages
package:
	poetry check
	poetry run pip check
	poetry run pip-audit

# Run all checks
check: lint package test

