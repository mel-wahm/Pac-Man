run:
	@uv run pac-man.py config.json
install:
	@uv sync
debug:
	@uv run python -m pdb pac-man.py config.json
clean:
	@pyclean .
	@rm -rf .mypy_cache

lint:
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
