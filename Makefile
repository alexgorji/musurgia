.PHONY: test
test:
	uv sync --group test
	uv run pytest -m "not wip"

.PHONY: test-only
test-only:
	uv sync --group test
	uv run pytest -m "only"

.PHONY: testgraphics
testgraphics:
	uv sync --group test
	uv run pytest musurgia/tests/graphics -m "not wip"

.PHONY: typecheck
typecheck:
	uv run mypy musurgia

.PHONY: pre-push-hook
pre-push-hook:
	uv run mypy --strict musurgia/graphics
	uv sync --group test
	uv run pytest -m "not wip"

