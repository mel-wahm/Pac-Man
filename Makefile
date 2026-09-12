run:
	@uv run pac-man.py config.json
install:
	@uv sync
debug:
	@uv run python -m pdb pac-man.py config.json
clean:
	@uv run pyclean .
	@rm -rf .mypy_cache

lint:
	@uv run flake8 .
	@uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
