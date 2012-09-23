# $Id: __init__.py 6328 2010-05-23 21:20:29Z gbrandl $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
REP HTML Writer.
"""

__docformat__ = 'reStructuredText'


import sys
import os
import os.path
import codecs
import docutils
from docutils import frontend, nodes, utils, writers
from docutils.writers import html4css1


class Writer(html4css1.Writer):

    default_stylesheet = 'rep.css'

    default_stylesheet_path = utils.relative_path(
        os.path.join(os.getcwd(), 'dummy'),
        os.path.join(os.path.dirname(__file__), default_stylesheet))

    default_template = 'template.rst'

    default_template_path = utils.relative_path(
        os.path.join(os.getcwd(), 'dummy'),
        os.path.join(os.path.dirname(__file__), default_template))

    settings_spec = html4css1.Writer.settings_spec + (
        'REP/HTML-Specific Options',
        'For the REP/HTML writer, the default value for the --stylesheet-path '
        'option is "%s", and the default value for --template is "%s". '
        'See HTML-Specific Options above.'
        % (default_stylesheet_path, default_template_path),
        (('ROS\'s home URL.  Default is "http://ros.org".',
          ['--ros-home'],
          {'default': 'http://ros.org', 'metavar': '<URL>'}),
         ('Home URL prefix for REPs.  Default is "." (current directory).',
          ['--rep-home'],
          {'default': '.', 'metavar': '<URL>'}),
         # For testing.
         (frontend.SUPPRESS_HELP,
          ['--no-random'],
          {'action': 'store_true', 'validator': frontend.validate_boolean}),))

    settings_default_overrides = {'stylesheet_path': default_stylesheet_path,
                                  'template': default_template_path,}

    relative_path_settings = (html4css1.Writer.relative_path_settings
                              + ('template',))

    config_section = 'rep_html writer'
    config_section_dependencies = ('writers', 'html4css1 writer')

    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = HTMLTranslator

    def interpolation_dict(self):
        subs = html4css1.Writer.interpolation_dict(self)
        settings = self.document.settings
        roshome = settings.ros_home
        subs['roshome'] = roshome
        subs['rephome'] = settings.rep_home
        if roshome == '..':
            subs['repindex'] = '.'
        else:
            subs['repindex'] = roshome + '/reps/rep-0000.html'
        index = self.document.first_child_matching_class(nodes.field_list)
        header = self.document[index]
        self.repnum = header[0][1].astext()
        subs['rep'] = self.repnum
        if settings.no_random:
            subs['banner'] = 0
        else:
            import random
            subs['banner'] = random.randrange(64)
        try:
            subs['repnum'] = '%04i' % int(self.repnum)
        except ValueError:
            subs['repnum'] = self.repnum
        self.title = header[1][1].astext()
        subs['title'] = self.title
        subs['body'] = ''.join(
            self.body_pre_docinfo + self.docinfo + self.body)
        return subs

    def assemble_parts(self):
        html4css1.Writer.assemble_parts(self)
        self.parts['title'] = [self.title]
        self.parts['repnum'] = self.repnum


class HTMLTranslator(html4css1.HTMLTranslator):

    def depart_field_list(self, node):
        html4css1.HTMLTranslator.depart_field_list(self, node)
        if 'rfc2822' in node['classes']:
             self.body.append('<hr />\n')
