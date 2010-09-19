#!/usr/bin/env python2.5
"""Auto-generate REP 0 (REP index).

Generating the REP index is a multi-step process.  To begin, you must first
parse the REP files themselves, which in and of itself takes a couple of steps:

    1. Parse metadata.
    2. Validate metadata.

With the REP information collected, to create the index itself you must:

    1. Output static text.
    2. Format an entry for the REP.
    3. Output the REP (both by category and numerical index).

"""
from __future__ import absolute_import, with_statement

import sys
import os
import codecs

from operator import attrgetter

from rep0.output import write_rep0
from rep0.rep import REP, REPError


def main(argv):
    if not argv[1:]:
        path = '.'
    else:
        path = argv[1]

    reps = []
    if os.path.isdir(path):
        for file_path in os.listdir(path):
            abs_file_path = os.path.join(path, file_path)
            if not os.path.isfile(abs_file_path):
                continue
            if file_path.startswith("rep-") and file_path.endswith(".txt"):
                with codecs.open(abs_file_path, 'r', encoding='UTF-8') as rep_file:
                    try:
                        rep = REP(rep_file)
                        if rep.number != int(file_path[4:-4]):
                            raise REPError('REP number does not match file name',
                                           file_path, rep.number)
                        reps.append(rep)
                    except REPError, e:
                        errmsg = "Error processing REP %s (%s), excluding:" % \
                            (e.number, e.filename)
                        print >>sys.stderr, errmsg, e
                        sys.exit(1)
        reps.sort(key=attrgetter('number'))
    elif os.path.isfile(path):
        with open(path, 'r') as rep_file:
            reps.append(REP(rep_file))
    else:
        raise ValueError("argument must be a directory or file path")

    with codecs.open('rep-0000.txt', 'w', encoding='UTF-8') as rep0_file:
        write_rep0(reps, rep0_file)

if __name__ == "__main__":
    main(sys.argv)
