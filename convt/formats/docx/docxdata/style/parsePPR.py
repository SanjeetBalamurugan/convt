"""
 Copyright © 2026 Sanjeet Balamurugan. All rights reserved.
 This source code is licensed under the Orion License.
 Commercial use, commercialisation, and revenue generation are strictly prohibited.
 Personal, non-commercial use and modification are permitted.


 Any distributed modifications must attribute "Convt" and link to the homepage at "https://github.com/SanjeetBalamurugan/convt".
 See the root LICENSE file for details.
 """

import xml.etree.ElementTree as ET
from convt.formats.docx.docxdata.style.parseNumPR import parseStyles_numPr
from convt.formats.docx.docxdata.stylesData import Alignment, BDRVal, SHDVal
from convt.parser.hxml import getAttr
from convt.formats.docx.docxdata.defaults import defaults_pPr

def parsePPRToggles(pPr: ET.Element, ns: dict) -> dict:
    toggles = ["keepNext", "keepLines", "widowControl", "suppressLineNumbers", "suppressHyphenation", "pageBreakBefore", "bidi"]
    result = {}

    for tag in toggles:
        element = pPr.find(f"w:{tag}", ns)
        if element is not None:
            val = getAttr(element, "w:val", ns)
            result[tag] = {
                "val": val.lower() in ["1", "true"] if val else True
            }
        else:
            result[tag] = { "val": None }

    return result

def parseSpacing(spacing: ET.Element, ns: dict) -> dict:
    before_raw = getAttr(spacing, "w:before", ns)
    before = int(before_raw) if before_raw is not None else None

    before_lines_raw = getAttr(spacing, "w:beforeLines", ns)
    beforeLines = int(before_lines_raw) if before_lines_raw is not None else None

    after_raw = getAttr(spacing, "w:after", ns)
    after = int(after_raw) if after_raw is not None else None

    after_lines_raw = getAttr(spacing, "w:afterLines", ns)
    afterLines = int(after_lines_raw) if after_lines_raw is not None else None

    line_raw = getAttr(spacing, "w:line", ns)
    line = int(line_raw) if line_raw is not None else None
    
    lineRule = getAttr(spacing, "w:lineRule", ns)

    return {
        "before": before,
        "beforeLines": beforeLines,
        "after": after,
        "afterLines": afterLines,
        "line": line,
        "lineRule": lineRule
    }

def parseIndentation(ind: ET.Element, ns: dict) -> dict:
    left_raw = getAttr(ind, "w:left", ns)
    left = int(left_raw) if left_raw is not None else None

    right_raw = getAttr(ind, "w:right", ns)
    right = int(right_raw) if right_raw is not None else None

    hanging_raw = getAttr(ind, "w:hanging", ns)
    hanging = int(hanging_raw) if hanging_raw is not None else None

    first_line_raw = getAttr(ind, "w:firstLine", ns)
    firstLine = int(first_line_raw) if first_line_raw is not None else None

    return {
        "left": left,
        "right": right,
        "hanging": hanging,
        "firstLine": firstLine
    }

def parsePPRSHD(shd: ET.Element, ns:dict) -> dict:
    shd_val = getAttr(shd, "w:val", ns)
    val = SHDVal(shd_val) if shd_val is not None else None
    
    fill = getAttr(shd, "w:fill", ns) or "auto"

    return {
        "val": val,
        "fill": fill
    }

def parseFramePr(framePr: ET.Element, ns: dict) -> dict:
    # Explicit integer layouts (Coordinates, Widths, Heights, Paddings)
    h_raw = getAttr(framePr, "w:h", ns)
    h = int(h_raw) if h_raw is not None else None

    h_space_raw = getAttr(framePr, "w:hSpace", ns)
    hSpace = int(h_space_raw) if h_space_raw is not None else None

    v_space_raw = getAttr(framePr, "w:vSpace", ns)
    vSpace = int(v_space_raw) if v_space_raw is not None else None

    w_raw = getAttr(framePr, "w:w", ns)
    w = int(w_raw) if w_raw is not None else None

    x_raw = getAttr(framePr, "w:x", ns)
    x = int(x_raw) if x_raw is not None else None

    y_raw = getAttr(framePr, "w:y", ns)
    y = int(y_raw) if y_raw is not None else None

    # Structural layout rule strings
    dropCap = getAttr(framePr, "w:dropCap", ns)
    hRule = getAttr(framePr, "w:hRule", ns)
    wrap = getAttr(framePr, "w:wrap", ns)

    x_align_raw = getAttr(framePr, "w:xAlign", ns)
    xAlign = Alignment(x_align_raw) if x_align_raw is not None else None

    y_align_raw = getAttr(framePr, "w:yAlign", ns)
    yAlign = Alignment(y_align_raw) if y_align_raw is not None else None

    return {
        "dropCap": dropCap,
        "h": h,
        "hRule": hRule,
        "hSpace": hSpace,
        "vSpace": vSpace,
        "w": w,
        "wrap": wrap,
        "x": x,
        "xAlign": xAlign,
        "y": y,
        "yAlign": yAlign
    }

def parsePPRBDR(pBdr: ET.Element, ns: dict) -> dict:
    sides = ["top", "left", "bottom", "right", "between", "bar"]
    result = {}

    for side in sides:
        element = pBdr.find(f"w:{side}", ns)
        if element is not None:
            bdr_val = getAttr(element, "w:val", ns)
            val = BDRVal(bdr_val) if bdr_val is not None else BDRVal("none")
            
            sz_raw = getAttr(element, "w:sz", ns)
            sz = int(sz_raw) if sz_raw is not None else 2
            
            space_raw = getAttr(element, "w:space", ns)
            space = int(space_raw) if space_raw is not None else 0
            
            color = getAttr(element, "w:color", ns) or "auto"
            
            result[side] = {
                "val": val,
                "sz": sz,
                "space": space,
                "color": color
            }
        else:
            result[side] = None

    return result

def parseStyles_pPr(pPr: ET.Element, ns: dict) -> dict:
    output = {}

    spacing = pPr.find("w:spacing", ns)
    ind = pPr.find("w:ind", ns)
    shd = pPr.find("w:shd", ns)
    pBdr = pPr.find("w:pBdr", ns)
    framePr = pPr.find("w:framePr", ns)
    numPr = pPr.find("w:numPr", ns)

    output["spacing"] = parseSpacing(spacing, ns) if spacing is not None else defaults_pPr["spacing"]
    output["ind"] = parseIndentation(ind, ns) if ind is not None else defaults_pPr["ind"]
    output["shd"] = parsePPRSHD(ind, ns) if shd is not None else defaults_pPr["shd"]
    output["pBdr"] = parsePPRBDR(ind, ns) if pBdr is not None else defaults_pPr["pBdr"]
    output["framePr"] = parseFramePr(ind, ns) if framePr is not None else defaults_pPr["framePr"]

    output["numPr"] = parseStyles_numPr(numPr, ns) if numPr is not None else defaults_pPr["numPr"]
    
    output |= parsePPRToggles(pPr, ns)
    return output