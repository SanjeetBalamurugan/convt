# Parser for word/styles.xml

import xml.etree.ElementTree as ET
from zipfile import ZipFile
from convt.formats.docx.docxdata.style.parsePPR import parseStyles_pPr
from convt.formats.docx.docxdata.style.parseRPR import parseStyles_rPr
from convt.formats.docx.docxdata.stylesData import StyleType
from convt.parser.hxml import getAttr, getNameSpaces

def parsePRStyles(element: ET.Element, ns: dict) -> dict:
    # <w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia" w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi"/>
    output = {}
    
    rPr = element.find("w:rPr", ns) # Run Properties
    if rPr is not None:
        output["rPr"] = parseStyles_rPr(rPr, ns) or {}

    pPr = element.find("w:pPr", ns) # Run Properties
    if pPr is not None:
        output["pPr"] = parseStyles_pPr(pPr, ns) or {}
    
    return output

# for w:style
def parseStyles(style: ET.Element[str], ns: dict) -> dict:
    type = StyleType(getAttr(style, "w:type", ns))
    styleId = getAttr(style, "w:styleId", ns)
    default = bool(getAttr(style, "w:default", ns))
    customStyle = bool(getAttr(style, "w:customStyle", ns))

    # TODO: make the childeren
    name_val = getAttr(style.find("w:name", ns), "w:val", ns)
    uiPriority = int(getAttr(style.find("w:uiPriority", ns), "w:val", ns) or 1)

    out = {
        "styleId": styleId,
        "type": type,
        "default": default,
        "customStyle": customStyle,

        "uiPriority": { "val": uiPriority },
        "name": { "val": name_val }
    }

    bools = [ "qFormat", "autoRedefine", "hidden", "semiHidden", "unhideWhenUsed" ]
    for tag in bools:
        element = style.find(f"w:{tag}", ns)
        if element is not None:
            val = getAttr(element, "w:val", ns)
            out[tag] = {
                "val": val.lower() in ["1", "true"] if val else True
            }
        else:
            out[tag] = { "val": None }

    # Assuming the output styleID already exists, and importantly these are required for a basic w:style tag (except link and aliases)
    val_fields = [ "basedOn", "next", "aliases", "link" ]
    for tag in val_fields:
        element = getAttr(style.find(f"w:{tag}", ns), "w:val", ns)
        out[tag] = { "val": element }

    if not default and type == StyleType.PARAGRAPH:
        pPr = style.find("w:pPr", ns)
        out["pPr"] = parseStyles_pPr(pPr, ns) if (pPr is not None and type != StyleType.CHARACTER) else None

        rPr = style.find("w:rPr", ns)
        out["rPr"] = parseStyles_rPr(rPr, ns) if rPr is not None else None

    return out

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

            defaults_rPr = parsePRStyles(rPrDefault, namespaces)
            defaults_pPr = parsePRStyles(pPrDefault, namespaces)

            for style in root.findall("w:style", namespaces):
                styleId = getAttr(style, "w:styleId", namespaces)
                styles[styleId] = parseStyles(style, namespaces)
                
    print(styles["Normal"])
    print()
    print()
    print(styles["Heading1"])
    return styles