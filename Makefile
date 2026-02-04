.PHONY: test
test:
	uv sync --group test
	uv run pytest

.PHONY: typecheck
typecheck:
	uv run mypy ./musurgia