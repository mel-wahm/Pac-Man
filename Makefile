run:
	@python3 -m Src
install:
	@pip install arcade
	@pip install pyclean
it: run
	@clear
clean:
	@pyclean .

lint:
	@flake8 Src
