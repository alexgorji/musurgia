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

.PHONY: type-check
type-check:
	uv run mypy musurgia --strict


.PHONY: pre-push-hook
pre-push-hook:
	$(MAKE) type-check
	uv sync --group test
	uv run pytest -m "not wip"


