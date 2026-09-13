run:
	@uv run pac-man.py config.json
install:
	@uv sync
debug:
	@uv run python -m pdb pac-man.py config.json
clean:
	@uv run pyclean .
	@rm -rf .mypy_cache
	@rm -rf .flake8

lint:
	@uv run flake8 src pac-man.py
	@uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
