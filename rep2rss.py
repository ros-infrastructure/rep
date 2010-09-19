#!/usr/bin/env python

import os, glob, time, datetime, stat, re, sys
import codecs
import PyRSS2Gen as rssgen

RSS_PATH = os.path.join(sys.argv[1], 'reps.rss')

def firstline_startingwith(full_path, text):
    for line in codecs.open(full_path, encoding="utf-8"):
        if line.startswith(text):
            return line[len(text):].strip()
    return None

# get list of reps with creation time (from "Created:" string in rep .txt)
reps = glob.glob('rep-*.txt')
def rep_creation_dt(full_path):
    created_str = firstline_startingwith(full_path, 'Created:')
    # bleh, I was hoping to avoid re but some Reps editorialize
    # on the Created line
    m = re.search(r'''(\d+-\w+-\d{4})''', created_str)
    if not m:
        # some older ones have an empty line, that's okay, if it's old
        # we ipso facto don't care about it.
        # "return None" would make the most sense but datetime objects
        # refuse to compare with that. :-|
        return datetime.datetime(*time.localtime(0)[:6])
    created_str = m.group(1)
    try:
        t = time.strptime(created_str, '%d-%b-%Y')
    except ValueError:
        t = time.strptime(created_str, '%d-%B-%Y')
    return datetime.datetime(*t[:6])
reps_with_dt = [(rep_creation_dt(full_path), full_path) for full_path in reps]
# sort reps by date, newest first
reps_with_dt.sort(reverse=True)

# generate rss items for 10 most recent reps
items = []
for dt, full_path in reps_with_dt[:10]:
    try:
        n = int(full_path.split('-')[-1].split('.')[0])
    except ValueError:
        pass
    title = firstline_startingwith(full_path, 'Title:')
    author = firstline_startingwith(full_path, 'Author:')
    url = 'http://ros.org/reps/rep-%0.4d' % n
    item = rssgen.RSSItem(
        title = 'REP %d: %s' % (n, title),
        link = url,
        description = 'Author: %s' % author,
        guid = rssgen.Guid(url),
        pubDate = dt)
    items.append(item)

# the rss envelope
desc = """
Newest ROS Enhancement Proposals (REPs) - Information on new
language features, and some meta-information like release
procedure and schedules
""".strip()
rss = rssgen.RSS2(
    title = 'Newest ROS Reps',
    link = 'http://ros.org/reps',
    description = desc,
    lastBuildDate = datetime.datetime.now(),
    items = items)

file(RSS_PATH, 'w').write(rss.to_xml())
