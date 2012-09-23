# -*- coding: utf-8 -*-

# Original authors:
# David Goodger <goodger@python.org>,
# Barry Warsaw <barry@python.org>


title_length = 55
column_format = (u' %(type)1s%(status)1s %(number)4s  %(title)-' +
                    unicode(title_length) + u's %(authors)-s')

header = u"""REP: 0
Title: Index of ROS Enhancement Proposals (REPs)
Last-Modified: %s
Author: ROS Developers
Status: Active
Type: Informational
Created: 13-Jul-2000
"""

intro = u"""
    The REP contains the index of all ROS Enhancement Proposals,
    known as REPs.  REP numbers are assigned by the REP Editor, and
    once assigned are never changed.  The GIT history[1] of the REP
    texts represent their historical record.

"""

references = u"""
    [1] View REP history online
        https://github.com/ros-infrastructure/rep
"""

footer = u"""
Local Variables:
mode: indented-text
indent-tabs-mode: nil
sentence-end-double-space: t
fill-column: 70
coding: utf-8
End:"""
