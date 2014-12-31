
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from citeproc.py2compat import *

try:
    from html import escape
except ImportError:
    from cgi import escape


def preformat(text):
    return escape(str(text), quote=False)


class TagWrapper(str):
    tag = None
    attributes = None
    datetime_classes = ['issued', 'accessed', 'event-date', 'original-date', 'submitted']

    @classmethod
    def _wrap(cls, text, attributes=None):
        tag = cls.tag or 'span'
        
        if attributes == None:
            attributes = {}
            
        if cls.attributes:
            attributes.update(cls.attributes)
        
        class_value = attributes.get('class', None)
        
        if class_value:        
            if class_value in cls.datetime_classes:
                tag = 'time'
                if class_value == 'issued':
                    attributes['class'] = 'dt-published'
                if class_value == 'accessed':
                    attributes['class'] = 'dt-accessed'
        
            if class_value == 'title':
                tag = 'cite'
                attributes['class'] = 'p-name'
        
            if class_value == 'author':
                attributes['class'] = 'p-author'
                        
        if tag == 'a':
            attributes['class'] = 'u-url'
        
        if attributes:
            attrib = ' ' + ' '.join(['{}="{}"'.format(key, value)
                                     for key, value in attributes.items()])
        else:
            attrib = ''
        
        return '<{tag}{attrib}>{text}</{tag}>'.format(tag=tag,
                                                      attrib=attrib,text=text)

    def __new__(cls, text, attributes=None):
        return super(TagWrapper, cls).__new__(cls, cls._wrap(text, attributes))

class Span(TagWrapper):
    pass

class Url(TagWrapper):
    tag = 'a'

class Italic(TagWrapper):
    tag = 'i'

class Oblique(Italic):
    pass

class Bold(TagWrapper):
    tag = 'b'


class Light(TagWrapper):
    tag = 'l'


class Underline(TagWrapper):
    tag = 'u'


class Superscript(TagWrapper):
    tag = 'sup'


class Subscript(TagWrapper):
    tag = 'sub'


class SmallCaps(TagWrapper):
    tag = 'span'
    attributes = {'style': 'font-variant:small-caps;'}