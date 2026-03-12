.PHONY: test
test:
	uv sync --group test
	uv run pytest

.PHONY: testgraphics
testgraphics:
	uv sync --group test
	uv run pytest musurgia/tests/graphics

.PHONY: typecheck
typecheck:
	uv run mypy musurgia