#!/usr/bin/env python

"""
Pandoc filter to citeproc-py.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import sys
sys.path.insert(0, '../')
from citeproc.py2compat import *

# The references are parsed from a BibTeX database, so we import the
# corresponding parser.
from citeproc.source.bibtex import BibTeX

# Import the citeproc-py classes we'll use below.
from citeproc import CitationStylesStyle, CitationStylesBibliography
from citeproc import formatter
from citeproc import Citation, CitationItem

from pandocfilters import walk, RawInline, RawBlock, Cite, Span, Para, Div, attributes
import json
import logging

# Parse the BibTeX database.

bib_source = BibTeX('ascii.bib')

# load a CSL style (from the current directory)

bib_style = CitationStylesStyle('/Users/nick/.pandoc/pandoc-templates/csl/' + 'apsa.csl', validate=False)


# Create the citeproc-py bibliography, passing it the:
# * CitationStylesStyle,
# * BibliographySource (BibTeX in this case), and
# * a formatter (plain, html, or you can write a custom formatter)

bibliography = CitationStylesBibliography(bib_style, bib_source,
                                          formatter.html)

citations = []
counter = 0

def citation_register(key, value, format, meta):
    if key == 'Cite':
        citation = Citation([CitationItem(value[0][0]['citationId'])])
        bibliography.register(citation)
        citations.append(citation)

def citation_replace(key, value, format, meta):
    if key == 'Cite':
        global counter
        citation = citations[counter]
        counter = counter + 1
        return Cite(value[0], [RawInline('html', bibliography.cite(citation, None))])

def add_bibliography(key, value, format, meta):
    if key == 'Cite':
        global counter
        citation = citations[counter]
        counter = counter + 1
        return Cite(value[0], [RawInline('html', bibliography.cite(citation, None))])

if __name__ == "__main__":
    # follows the basic model of pandocfilters toJSONFilter, but we do multiple passes
    doc = json.loads(sys.stdin.read())
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""
    altered = walk(doc, citation_register, format, doc[0]['unMeta'])
    second = walk(altered, citation_replace, format, doc[0]['unMeta'])
    
    references = []
    for item in bibliography.bibliography():
        references.append(Para([RawInline('html', str(item))]))
        
    second[1].extend(references)
    
    json.dump(second, sys.stdout)