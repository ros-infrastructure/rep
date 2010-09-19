"""Code to handle the output of REP 0."""
import datetime
import sys
import unicodedata

from operator import attrgetter

from . import constants
from .rep import REP, REPError


indent = u' '

def write_column_headers(output):
    """Output the column headers for the REP indices."""
    column_headers = {'status': u'', 'type': u'', 'number': u'num',
                        'title': u'title', 'authors': u'owner'}
    print>>output, constants.column_format % column_headers
    underline_headers = {}
    for key, value in column_headers.items():
        underline_headers[key] = unicode(len(value) * '-')
    print>>output, constants.column_format % underline_headers


def sort_reps(reps):
    """Sort REPs into meta, informational, accepted, open, finished,
    and essentially dead."""
    meta = []
    info = []
    accepted = []
    open_ = []
    finished = []
    dead = []
    for rep in reps:
        # Order of 'if' statement important.  Key Status values take precedence
        # over Type value, and vice-versa.
        if rep.type_ == 'Process':
            meta.append(rep)
        elif rep.status == 'Draft':
            open_.append(rep)
        elif rep.status in ('Rejected', 'Withdrawn', 'Deferred',
                'Incomplete', 'Replaced'):
            dead.append(rep)
        elif rep.type_ == 'Informational':
            info.append(rep)
        elif rep.status in ('Accepted', 'Active'):
            accepted.append(rep)
        elif rep.status == 'Final':
            finished.append(rep)
        else:
            raise REPError("unsorted (%s/%s)" %
                           (rep.type_, rep.status),
                           rep.filename, rep.number)
    return meta, info, accepted, open_, finished, dead


def verify_email_addresses(reps):
    authors_dict = {}
    for rep in reps:
        for author in rep.authors:
            # If this is the first time we have come across an author, add him.
            if author not in authors_dict:
                authors_dict[author] = [author.email]
            else:
                found_emails = authors_dict[author]
                # If no email exists for the author, use the new value.
                if not found_emails[0]:
                    authors_dict[author] = [author.email]
                # If the new email is an empty string, move on.
                elif not author.email:
                    continue
                # If the email has not been seen, add it to the list.
                elif author.email not in found_emails:
                    authors_dict[author].append(author.email)

    valid_authors_dict = {}
    too_many_emails = []
    for author, emails in authors_dict.items():
        if len(emails) > 1:
            too_many_emails.append((author.first_last, emails))
        else:
            valid_authors_dict[author] = emails[0]
    if too_many_emails:
        err_output = []
        for author, emails in too_many_emails:
            err_output.append("    %s: %r" % (author, emails))
        raise ValueError("some authors have more than one email address "
                         "listed:\n" + '\n'.join(err_output))

    return valid_authors_dict


def sort_authors(authors_dict):
    authors_list = authors_dict.keys()
    authors_list.sort(key=attrgetter('sort_by'))
    return authors_list

def normalized_last_first(name):
    return len(unicodedata.normalize('NFC', name.last_first))


def write_rep0(reps, output=sys.stdout):
    today = datetime.date.today().strftime("%Y-%m-%d")
    print>>output, constants.header % today
    print>>output
    print>>output, u"Introduction"
    print>>output, constants.intro
    print>>output
    print>>output, u"Index by Category"
    print>>output
    write_column_headers(output)
    meta, info, accepted, open_, finished, dead = sort_reps(reps)
    print>>output
    print>>output, u" Meta-REPs (REPs about REPs or Processes)"
    print>>output
    for rep in meta:
        print>>output, unicode(rep)
    print>>output
    print>>output, u" Other Informational REPs"
    print>>output
    for rep in info:
        print>>output, unicode(rep)
    print>>output
    print>>output, u" Accepted REPs (accepted; may not be implemented yet)"
    print>>output
    for rep in accepted:
        print>>output, unicode(rep)
    print>>output
    print>>output, u" Open REPs (under consideration)"
    print>>output
    for rep in open_:
        print>>output, unicode(rep)
    print>>output
    print>>output, u" Finished REPs (done, implemented in code repository)"
    print>>output
    for rep in finished:
        print>>output, unicode(rep)
    print>>output
    print>>output, u" Deferred, Abandoned, Withdrawn, and Rejected REPs"
    print>>output
    for rep in dead:
        print>>output, unicode(rep)
    print>>output
    print>>output
    print>>output, u" Numerical Index"
    print>>output
    write_column_headers(output)
    prev_rep = 0
    for rep in reps:
        if rep.number - prev_rep > 1:
            print>>output
        print>>output, unicode(rep)
        prev_rep = rep.number
    print>>output
    print>>output
    print>>output, u"Key"
    print>>output
    for type_ in REP.type_values:
        print>>output, u"    %s - %s REP" % (type_[0], type_)
    print>>output
    for status in REP.status_values:
        print>>output, u"    %s - %s proposal" % (status[0], status)

    print>>output
    print>>output
    print>>output, u"Owners"
    print>>output
    authors_dict = verify_email_addresses(reps)
    max_name = max(authors_dict.keys(), key=normalized_last_first)
    max_name_len = len(max_name.last_first)
    print>>output, u"    %s  %s" % ('name'.ljust(max_name_len), 'email address')
    print>>output, u"    %s  %s" % ((len('name')*'-').ljust(max_name_len),
                                    len('email address')*'-')
    sorted_authors = sort_authors(authors_dict)
    for author in sorted_authors:
        # Use the email from authors_dict instead of the one from 'author' as
        # the author instance may have an empty email.
        print>>output, (u"    %s  %s" %
                (author.last_first.ljust(max_name_len), authors_dict[author]))
    print>>output
    print>>output
    print>>output, u"References"
    print>>output
    print>>output, constants.references
    print>>output, constants.footer
