SOURCES = $(wildcard *.py)
DOCTESTS = $(SOURCES:.py=.doctest)
LINT = $(SOURCES:.py=.pylint)
all: $(DOCTESTS) $(LINT)
%.doctest: %.py
	python3 -m doctest $<
%.pylint: %.py
	pylint3 $<
