# Rules to only make the required HTML versions, not all of them,
# without the user having to keep track of which.
#
# Not really important, but convenient.

REP2HTML=rep2html.py

PYTHON=python

.SUFFIXES: .txt .html

.txt.html:
	@$(PYTHON) $(REP2HTML) $<

REPS=$(filter-out rep-0000.txt,$(wildcard rep-????.txt))

TARGETS=$(REPS:.txt=.html) rep-0000.html

all: rep-0000.txt $(TARGETS)

$(TARGETS) rep-0000.html1: rep2html.py

rep-0000.txt: $(REPS)
	$(PYTHON) genrepindex.py .

install:
	echo "Installing is not necessary anymore. It will be done in post-commit."

clean:
	-rm *.html
	-rm rep-0000.txt

update:
	svn update

propcheck:
	$(PYTHON) propcheck.py

upload:
	rsync *.txt *.html wgs32.willowgarage.com:/var/www/www.ros.org/html/reps
