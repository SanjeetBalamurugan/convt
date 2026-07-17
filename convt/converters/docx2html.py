import xml.etree.ElementTree as ET
from enum import Enum
import re

from convt.formats.docx import extractFonts
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

        
        