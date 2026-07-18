"""
 Copyright © 2026 Sanjeet Balamurugan. All rights reserved.
 This source code is licensed under the Orion License.
 Commercial use, commercialisation, and revenue generation are strictly prohibited.
 Personal, non-commercial use and modification are permitted.


 Any distributed modifications must attribute "Convt" and link to the homepage at "https://github.com/SanjeetBalamurugan/convt".
 See the root LICENSE file for details.
 """

import os
import xml.etree.ElementTree as ET
from convt.formats.docx.docxdata.themeDate import SystemColorVal, ThemeColorElement
from convt.parser.hxml import getAttr, getNameSpaces
from zipfile import ZipFile

def parseColorValue(color_el: ET.Element, ns: dict) -> dict | None:
    if color_el is None:
        return None
        
    sys_clr = color_el.find("a:sysClr", ns)
    if sys_clr is not None:
        val_raw = sys_clr.get("val") or getAttr(sys_clr, "a:val", ns)
        last_clr = sys_clr.get("lastClr") or getAttr(sys_clr, "a:lastClr", ns)
        return {
            "type": "sysClr",
            "val": SystemColorVal(val_raw) if val_raw is not None else None,
            "lastClr": last_clr
        }
        
    srgb_clr = color_el.find("a:srgbClr", ns)
    if srgb_clr is not None:
        return {
            "type": "srgbClr",
            "val": srgb_clr.get("val") or getAttr(srgb_clr, "a:val", ns)
        }
        
    return None

def parseColorScheme(clr_scheme: ET.Element, ns: dict) -> dict | None:
    if clr_scheme is None:
        return None
        
    name = clr_scheme.get("name") or getAttr(clr_scheme, "a:name", ns)
    colors = {}
    
    for element_type in ThemeColorElement:
        element_node = clr_scheme.find(f"a:{element_type.value}", ns)
        if element_node is not None:
            colors[element_type.value] = parseColorValue(element_node, ns)
        else:
            colors[element_type.value] = None
            
    return {
        "name": name,
        "colors": colors
    }

def parseFontElement(font_container: ET.Element, ns: dict) -> dict | None:
    if font_container is None:
        return None
        
    latin_el = font_container.find("a:latin", ns)
    ea_el = font_container.find("a:ea", ns)
    cs_el = font_container.find("a:cs", ns)
    
    font_scripts = []
    for f_el in font_container.findall("a:font", ns):
        font_scripts.append({
            "script": f_el.get("script") or getAttr(f_el, "a:script", ns),
            "typeface": f_el.get("typeface") or getAttr(f_el, "a:typeface", ns)
        })
        
    return {
        "latin": latin_el.get("typeface") or getAttr(latin_el, "a:typeface", ns) if latin_el is not None else None,
        "ea": ea_el.get("typeface") or getAttr(ea_el, "a:typeface", ns) if ea_el is not None else None,
        "cs": cs_el.get("typeface") or getAttr(cs_el, "a:typeface", ns) if cs_el is not None else None,
        "scripts": font_scripts
    }

def parseFontScheme(font_scheme: ET.Element, ns: dict) -> dict | None:
    if font_scheme is None:
        return None
        
    name = font_scheme.get("name") or getAttr(font_scheme, "a:name", ns)
    major_font_el = font_scheme.find("a:majorFont", ns)
    minor_font_el = font_scheme.find("a:minorFont", ns)
    
    return {
        "name": name,
        "majorFont": parseFontElement(major_font_el, ns),
        "minorFont": parseFontElement(minor_font_el, ns)
    }

def parseTheme(theme: ET.Element, ns: dict) -> dict:
    name = theme.get("name") or getAttr(theme, "a:name", ns)
    theme_elements = theme.find("a:themeElements", ns)
    
    clr_scheme = None
    font_scheme = None
    
    if theme_elements is not None:
        clr_scheme = parseColorScheme(theme_elements.find("a:clrScheme", ns), ns)
        font_scheme = parseFontScheme(theme_elements.find("a:fontScheme", ns), ns)
        
    return {
        "name": name,
        "clrScheme": clr_scheme,
        "fontScheme": font_scheme
    }

def extractTheme(document_path: str) -> dict:
    THEME_DIR = "word/theme/"
    themes = {}
    
    with ZipFile(document_path, "r") as zfile:
        fileList = zfile.namelist()
        theme_files = [f for f in fileList if f.startswith(THEME_DIR) and f.endswith(".xml")]
        
        if not theme_files:
            return {}

        for theme_path in theme_files:
            theme_key = os.path.splitext(os.path.basename(theme_path))[0]
            
            with zfile.open(theme_path) as themeFile:
                content = themeFile.read().decode("utf-8")
                root = ET.fromstring(content)
                namespaces = getNameSpaces(content)
                
                themes[theme_key] = parseTheme(root, namespaces)
                
    return themes