"""
 Copyright © 2026 Sanjeet Balamurugan. All rights reserved.
 This source code is licensed under the Orion License.
 Commercial use, commercialisation, and revenue generation are strictly prohibited.
 Personal, non-commercial use and modification are permitted.


 Any distributed modifications must attribute "Convt" and link to the homepage at "https://github.com/SanjeetBalamurugan/convt".
 See the root LICENSE file for details.
 """

import sys
import argparse
import re

from .importer import Importer
from .config import TerminalColors
from .converters.docx2html import Docx2HTML

from docx2python import docx2python


def main():
    parser = argparse.ArgumentParser(prog="convt",
                                    description="A CLI program that converts one file type to another.",
                                    epilog="Thanks For Using My Program")
    parser.add_argument("inputfilename")
    parser.add_argument("outputfilename")

    args = parser.parse_args()
    inputPath = Importer(args.inputfilename)
    outputPath = Importer(args.outputfilename)

    if inputPath.extension == ".docx" and outputPath.extension == ".html":
        converter = Docx2HTML(inputPath, outputPath)
        converter.Generate()
    
    return 0
