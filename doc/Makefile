# redirect to make it compatible with other packages generating documentation

SUBDIRS=$(wildcard ../rep-????)

html:
	mkdir -p _build/html
	cd .. && make all
	cp -R ../README.txt ../*.html ../*.js ../rep-0000.rst $(SUBDIRS) _build/html

upload:
	cd .. && make upload
