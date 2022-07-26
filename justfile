lint:
	poetry run mypy pynaptan tests/**/*.py
	poetry run flake8 pynaptan

unit:
	poetry run pytest

package:
	poetry check
	poetry run pip check
	poetry run safety check --full-report

test: lint package unit

