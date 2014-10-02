# $Id: rep.py 4564 2006-05-21 20:44:42Z wiemann $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""Python Enhancement Proposal (REP) Reader."""

__docformat__ = 'reStructuredText'


from docutils.readers import standalone
from docutils.transforms import frontmatter
import docutils_transforms_reps as reps
from docutils.parsers import rst


class Reader(standalone.Reader):

    supported = ('rep',)
    """Contexts this reader supports."""

    settings_spec = (
        'REP Reader Option Defaults',
        'The --rep-references and --rfc-references options (for the '
        'reStructuredText parser) are on by default.',
        ())

    config_section = 'rep reader'
    config_section_dependencies = ('readers', 'standalone reader')

    def get_transforms(self):
        transforms = standalone.Reader.get_transforms(self)
        # We have REP-specific frontmatter handling.
        transforms.remove(frontmatter.DocTitle)
        transforms.remove(frontmatter.SectionSubTitle)
        transforms.remove(frontmatter.DocInfo)
        transforms.extend([reps.Headers, reps.Contents, reps.TargetNotes])
        return transforms

    settings_default_overrides = {'rep_references': 1, 'rfc_references': 1}

    inliner_class = rst.states.Inliner

    def __init__(self, parser=None, parser_name=None):
        """`parser` should be ``None``."""
        if parser is None:
            parser = rst.Parser(rfc2822=1, inliner=self.inliner_class())
        standalone.Reader.__init__(self, parser, '')
