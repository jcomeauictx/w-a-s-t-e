all: addressing.doctest
%.doctest: %.py
	python3 -m doctest $<
