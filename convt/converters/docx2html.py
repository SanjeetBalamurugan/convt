"""
 Copyright © 2026 Sanjeet Balamurugan. All rights reserved.
 This source code is licensed under the Orion License.
 Commercial use, commercialisation, and revenue generation are strictly prohibited.
 Personal, non-commercial use and modification are permitted.


 Any distributed modifications must attribute "Convt" and link to the homepage at "https://github.com/SanjeetBalamurugan/convt".
 See the root LICENSE file for details.
 """

import xml.etree.ElementTree as ET
from enum import Enum
import re

from convt.formats.docx.fonts import extractFonts
from convt.formats.docx.styles import extractStyles
from convt.formats.docx.theme import extractTheme
from convt.importer import Importer

import mammoth
from docx2python import docx2python
from bs4 import BeautifulSoup

namespaces = {}

class Docx2HTML:
    filePath = None
    outputPath = None
    media_dir = ""

    def __init__(self, inputPath: Importer, outputPath: Importer):
        self.filePath = inputPath.path
        self.outputPath = outputPath.path
        self.media_dir = self.filePath.stem + "_media"

    def Generate(self):
        media_rel_dir = self.outputPath.parent / self.media_dir
        print(media_rel_dir)

        fonts = extractFonts(self.filePath)
        body_matrix = None
        mammoth_html = ""

        styles = extractStyles(self.filePath)
        themes = extractTheme(self.filePath)

        print(themes)
        
        