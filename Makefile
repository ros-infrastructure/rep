# targets to generate an index, HTML files and upload them to the server

REP2HTML=rep2html.py

PYTHON=python

.SUFFIXES: .rst .html

.rst.html:
	@$(PYTHON) $(REP2HTML) $<

REPS=$(filter-out rep-0000.rst,$(wildcard rep-????.rst))

SUBDIRS=$(wildcard rep-????)

TARGETS=$(REPS:.rst=.html) rep-0000.html

all: rep-0000.rst $(TARGETS)

$(TARGETS): rep2html.py

rep-0000.rst: $(REPS)
	$(PYTHON) genrepindex.py .

clean:
	-rm *.html
	-rm rep-0000.rst

upload: all
	rsync -r *.html rep.css style.css rep-0000.rst $(SUBDIRS) root@wgs32.willowgarage.com:/var/www/www.ros.org/html/reps/new
