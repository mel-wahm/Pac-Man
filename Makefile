run:
	@python3 -m Src
it: run
	@clear
clean:
	@rm -rf .mypy_cache .ruff_cache __pycache__ Src/__pycache__

lint:
	@flake8 Src
