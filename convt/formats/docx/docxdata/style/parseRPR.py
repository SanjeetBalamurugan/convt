import xml.etree.ElementTree as ET
from convt.formats.docx.docxdata.defaults import defaults_rPr
from convt.formats.docx.docxdata.fontData import AsciiTheme, EastAsiaTheme, RFontHint
from convt.formats.docx.docxdata.stylesData import SHDVal, Theme, BDRVal
from convt.parser.hxml import getAttr


def parseRFonts(rFonts: ET.Element, ns: dict) -> dict:
    # Literal Font Attributes (Strings or None)
    w_ascii = getAttr(rFonts, "w:ascii", ns)
    hAnsi = getAttr(rFonts, "w:hAnsi", ns)
    eastAsia = getAttr(rFonts, "w:eastAsia", ns)
    cs = getAttr(rFonts, "w:cs", ns)

    ascii_theme_val = getAttr(rFonts, "w:asciiTheme", ns)
    asciiTheme = AsciiTheme(ascii_theme_val) if ascii_theme_val is not None else None

    h_ansi_theme_val = getAttr(rFonts, "w:hAnsiTheme", ns)
    hAnsiTheme = AsciiTheme(h_ansi_theme_val) if h_ansi_theme_val is not None else None

    east_asia_theme_val = getAttr(rFonts, "w:eastAsiaTheme", ns)
    eastAsiaTheme = EastAsiaTheme(east_asia_theme_val) if east_asia_theme_val is not None else None

    cs_theme_val = getAttr(rFonts, "w:cstheme", ns)
    csTheme = AsciiTheme(cs_theme_val) if cs_theme_val is not None else None

    hint_val = getAttr(rFonts, "w:hint", ns)
    hint = RFontHint(hint_val) if hint_val is not None else RFontHint("default")

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
            # OpenXML spec: absence of w:val inside toggle tag implies true
            result[tag] = {
                "val": val.lower() in ["1", "true"] if val else True
            }
        else:
            result[tag] = {"val": None}
            
    return result

def parseColor(color: ET.Element, ns: dict) -> dict:
    val = getAttr(color, "w:val", ns) or "auto"
    
    theme_val = getAttr(color, "w:theme", ns)
    theme = Theme(theme_val) if theme_val is not None else None
    
    tint_raw = getAttr(color, "w:themeTint", ns)
    themeTint = int(tint_raw, 16) if tint_raw is not None else None
    
    shade_raw = getAttr(color, "w:themeShade", ns)
    themeShade = int(shade_raw, 16) if shade_raw is not None else None

    return {
        "val": val,
        "theme": theme,
        "themeTint": themeTint,
        "themeShade": themeShade
    }

def parseSHD(shd: ET.Element, ns:dict) -> dict:
    shd_val = getAttr(shd, "w:val", ns)
    val = SHDVal(shd_val) if shd_val is not None else None
    
    color = getAttr(shd, "w:color", ns) or "auto"
    fill = getAttr(shd, "w:fill", ns) or "auto"

    return {
        "val": val,
        "color": color,
        "fill": fill
    }

def parseBDR(bdr: ET.Element, ns: dict) -> dict:
    bdr_val = getAttr(bdr, "w:val", ns)
    val = BDRVal(bdr_val) if bdr_val is not None else BDRVal("none")
    
    # sz = Size in 1/8 pt measurements (Integer)
    sz_raw = getAttr(bdr, "w:sz", ns)
    sz = int(sz_raw) if sz_raw is not None else 2
    
    # space = Distance padding from text in pt measurements (Integer)
    space_raw = getAttr(bdr, "w:space", ns)
    space = int(space_raw) if space_raw is not None else 0
    
    color = getAttr(bdr, "w:color", ns) or "auto"

    return {
        "val": val,
        "sz": sz,
        "space": space,
        "color": color
    }

def parseLang(lang: ET.Element, ns: dict) -> dict:
    # Language codes remain structural string markers (BCP 47 tags)
    val = getAttr(lang, "w:val", ns)
    eastAsia = getAttr(lang, "w:eastAsia", ns)
    bidi = getAttr(lang, "w:bidi", ns)

    return {
        "val": val,
        "eastAsia": eastAsia,
        "bidi": bidi
    }

def parseNumPr(numPr: ET.Element, ns: dict) -> dict:
    numId_el = numPr.find("w:numId", ns)
    ilvl_el = numPr.find("w:ilvl", ns)

    numId_raw = getAttr(numId_el, "w:val", ns) if numId_el is not None else None
    numId = int(numId_raw) if numId_raw is not None else None

    ilvl_raw = getAttr(ilvl_el, "w:val", ns) if ilvl_el is not None else None
    ilvl = int(ilvl_raw) if ilvl_raw is not None else None

    return {
        "numId": numId,
        "ilvl": ilvl
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
