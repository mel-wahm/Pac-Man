run:
	@python3 -m Src
install:
	@pip install arcade
	@pip install pyclean
it: run
	@clear
clean:
	@pyclean .
	@rm -rf .mypy_cache

lint:
	@flake8 Src
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
