# Parser for word/styles.xml

import xml.etree.ElementTree as ET
from zipfile import ZipFile
from convt.formats.docx.docxdata.style.parsePPR import parseStyles_pPr
from convt.formats.docx.docxdata.style.parseRPR import parseStyles_rPr
from convt.parser.hxml import getNameSpaces

def parseStyles(element: ET.Element, ns: dict) -> dict:
    # <w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia" w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/>
    output = {}
    
    rPr = element.find("w:rPr", ns) # Run Properties
    if rPr is not None:
        output["rPr"] = parseStyles_rPr(rPr, ns) or {}

    pPr = element.find("w:pPr", ns) # Run Properties
    if pPr is not None:
        output["pPr"] = parseStyles_pPr(pPr, ns) or {}
    
    return output

def extractStyles(document_path):
    STYLES_PATH = "word/styles.xml"
    styles = {}

    with ZipFile(document_path, "r") as zfile:
        fileList = zfile.namelist()
        
        if not STYLES_PATH in fileList:
            return {}

        with zfile.open(STYLES_PATH) as stylesFile:
            content = stylesFile.read().decode("utf-8")
            root = ET.fromstring(content)
            namespaces = getNameSpaces(content)

            docDefaults = root.find("w:docDefaults", namespaces)
            rPrDefault = docDefaults.find("w:rPrDefault", namespaces) # Default Run Properties
            pPrDefault = docDefaults.find("w:pPrDefault", namespaces) # Paragraph Properties Default

            defaults_rPr = parseStyles(rPrDefault, namespaces)
            defaults_pPr = parseStyles(pPrDefault, namespaces)

    
    print(defaults_pPr)
    return styles