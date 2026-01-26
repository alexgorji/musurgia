.PHONY: test
test:
	uv run pytest

.PHONY: typecheck
typecheck:
	uv run mypy ./musurgia