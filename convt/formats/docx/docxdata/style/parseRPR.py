import xml.etree.ElementTree as ET
from convt.formats.docx.docxdata.defaults import defaults_rPr
from convt.formats.docx.docxdata.fontData import AsciiTheme, EastAsiaTheme, RFontHint
from convt.formats.docx.docxdata.stylesData import SHDVal, Theme, BDRVal
from convt.parser.hxml import getAttr


def parseRFonts(rFonts: ET.Element, ns: dict) -> dict:
    # Literal Font Attributes
    w_ascii = getAttr(rFonts, "w:ascii", ns)
    hAnsi = getAttr(rFonts, "w:hAnsi", ns)
    eastAsia = getAttr(rFonts, "w:eastAsia", ns)
    cs = getAttr(rFonts, "w:cs", ns)

    # Theme Reference Attributes
    asciiTheme = AsciiTheme(getAttr(rFonts, "w:asciiTheme", ns))
    hAnsiTheme = AsciiTheme(getAttr(rFonts, "w:hAnsiTheme", ns))
    eastAsiaTheme = EastAsiaTheme(getAttr(rFonts, "w:eastAsiaTheme", ns))
    csTheme = AsciiTheme(getAttr(rFonts, "w:cstheme", ns))
    hint = RFontHint(getAttr(rFonts, "w:hint", ns) or "default")

    return {
        "ascii": w_ascii,
        "asciiTheme": asciiTheme,
        "hAnsi": hAnsi,
        "hAnsiTheme": hAnsiTheme,
        "eastAsia": eastAsia,
        "eastAsiaTheme": eastAsiaTheme,
        "cs": cs,
        "cstheme": csTheme,
        "hint": hint
    }

def parseToggleAttributes(rPr: ET.Element, ns: dict) -> dict:
    toggles = [
        "b", "bCs", "i", "iCs", "caps", "smallCaps", 
        "strike", "dstrike", "outline", "shadow", 
        "emboss", "imprint", "vanish", "webHidden"
    ]
    
    result = {}
    for tag in toggles:
        element = rPr.find(f"w:{tag}", ns)
        if element is not None:
            val = getAttr(element, "w:val", ns)
            result[tag] = {
                "val": val.lower() in ["1", "true"] if val else True
            }
        else:
            result[tag] = {"val": None}
            
    return result

def parseColor(color: ET.Element, ns: dict) -> dict:
    val = getAttr(color, "w:val", ns) or "auto"
    theme = Theme(getAttr(color, "w:theme", ns))
    themeTint = int(getAttr(color, "themeTint", ns) or 00, 16)
    themeShade = int(getAttr(color, "themeShade", ns) or 00, 16)

    return {
        "val": val,
        "theme": theme,
        "themeTint": themeTint,
        "themeShade": themeShade
    }

def parseSHD(shd: ET.Element, ns:dict):
    val = SHDVal(getAttr(shd, "w:val", ns))
    color = getAttr(shd, "w:color", ns) or "auto"
    fill = getAttr(shd, "w:fill", ns) or "auto"

    return {
        "val": val,
        "color": color,
        "fill": fill
    }

def parseBDR(bdr: ET.Element, ns: dict) -> dict:
    val = BDRVal(getAttr(bdr, "w:val", ns) or "none")
    sz = getAttr(bdr, "w:sz", ns) or 2
    space = getAttr(bdr, "w:space", ns) or 0
    color = getAttr(bdr, "w:color", ns) or "auto"

    return {
        "val": val,
        "sz": sz,
        "space": space,
        "color": color
    }


def parseLang(lang: ET.Element, ns: dict) -> dict:
    val = getAttr(lang, "w:val", ns)
    eastAsia = getAttr(lang, "w:eastAsia", ns)
    bidi = getAttr(lang, "w:bidi", ns)

    return {
        "val": val,
        "eastAsia": eastAsia,
        "bidi": bidi
    }


def parseStyles_rPr(rPr: ET.Element, ns: dict) -> dict | None:
    output = {}
    
    rFonts = rPr.find("w:rFonts", ns)
    color = rPr.find("w:color", ns)
    shd = rPr.find("w:shd", ns)
    lang = rPr.find("w:lang", ns)
    bdr = rPr.find("w:bdr", ns)

    output["rFonts"] = parseRFonts(rFonts, ns) if rFonts is not None else defaults_rPr["rFonts"]
    output["color"] = parseColor(color, ns) if color is not None else defaults_rPr["color"]
    output["shd"] = parseSHD(shd, ns) if shd is not None else defaults_rPr["shd"]
    output["lang"] = parseLang(lang, ns) if lang is not None else defaults_rPr["lang"]
    output["bdr"] = parseBDR(bdr, ns) if bdr is not None else defaults_rPr["bdr"]

    output |= parseToggleAttributes(rPr, ns)
    return output