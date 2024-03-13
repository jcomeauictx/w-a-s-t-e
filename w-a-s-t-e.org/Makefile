SERVER := $(shell basename $(PWD))
DOCROOT := /var/www/$(SERVER)
DRYRUN ?= --dry-run

upload:
	rsync -avuz \
	 $(DRYRUN) \
	 --exclude=.git \
	 --exclude=Makefile \
	 --exclude=README.md \
	 . $(SERVER):$(DOCROOT)/
/tmp/posthorn.png: posthorn.ps
	gs -sDEVICE=pnggray -sOutputFile=$@ -dNOPAUSE -dBATCH $<
posthorn.png: /tmp/posthorn.png
	convert $< -rotate -90 $@
