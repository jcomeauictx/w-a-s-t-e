SOURCES = $(wildcard *.py)
DOCTESTS = $(SOURCES:.py=.doctest)
LINT = $(SOURCES:.py=.pylint)
PYLINT ?= pylint3
all: $(DOCTESTS) $(LINT)
%.doctest: %.py
	python3 -m doctest $<
%.pylint: %.py
	$(PYLINT) $<
