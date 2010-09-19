# Rules to only make the required HTML versions, not all of them,
# without the user having to keep track of which.
#
# Not really important, but convenient.

REP2HTML=rep2html.py

PYTHON=python

.SUFFIXES: .txt .html

.txt.html:
	@$(PYTHON) $(REP2HTML) $<

TARGETS=$(patsubst %.txt,%.html,$(wildcard rep-????.txt)) rep-0000.html

all: rep-0000.txt $(TARGETS)

$(TARGETS): rep2html.py

rep-0000.txt: $(wildcard rep-????.txt)
	$(PYTHON) genrepindex.py .

install:
	echo "Installing is not necessary anymore. It will be done in post-commit."

clean:
	-rm rep-0000.txt
	-rm *.html

update:
	svn update

propcheck:
	$(PYTHON) propcheck.py
