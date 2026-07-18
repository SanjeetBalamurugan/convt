"""
 Copyright © 2026 Sanjeet Balamurugan. All rights reserved.
 This source code is licensed under the Orion License.
 Commercial use, commercialisation, and revenue generation are strictly prohibited.
 Personal, non-commercial use and modification are permitted.


 Any distributed modifications must attribute "Convt" and link to the homepage at "https://github.com/SanjeetBalamurugan/convt".
 See the root LICENSE file for details.
 """

import xml.etree.ElementTree as ET
from convt.parser.hxml import getAttr
from convt.formats.docx.docxdata.stylesData import BDRVal, CellVAlign, TableJc, TableWidthType, TblStylePrType

def parseBorderElement(bdr_el: ET.Element, ns: dict) -> dict | None:
    if bdr_el is None:
        return None
    val_raw = getAttr(bdr_el, "w:val", ns)
    val = BDRVal(val_raw) if val_raw is not None else BDRVal("none")
    sz_raw = getAttr(bdr_el, "w:sz", ns)
    space_raw = getAttr(bdr_el, "w:space", ns)
    
    return {
        "val": val,
        "sz": int(sz_raw) if sz_raw is not None else 2,
        "space": int(space_raw) if space_raw is not None else 0,
        "color": getAttr(bdr_el, "w:color", ns) or "auto"
    }

def parseTableBorders(tblBorders: ET.Element, ns: dict) -> dict:
    sides = ["top", "left", "bottom", "right", "insideH", "insideV"]
    return {side: parseBorderElement(tblBorders.find(f"w:{side}", ns), ns) for side in sides}

def parseTableProperties(tblPr: ET.Element, ns: dict) -> dict:
    w_el = tblPr.find("w:tblW", ns)
    tblW_type_raw = getAttr(w_el, "w:type", ns) if w_el is not None else None
    tblW = {
        "w": int(getAttr(w_el, "w:w", ns)) if getAttr(w_el, "w:w", ns) else None,
        "type": TableWidthType(tblW_type_raw) if tblW_type_raw is not None else None
    } if w_el is not None else None

    jc_el = tblPr.find("w:jc", ns)
    jc_raw = getAttr(jc_el, "w:val", ns) if jc_el is not None else None
    jc = TableJc(jc_raw) if jc_raw is not None else None

    borders_el = tblPr.find("w:tblBorders", ns)
    borders = parseTableBorders(borders_el, ns) if borders_el is not None else None

    return {
        "tblW": tblW,
        "jc": jc,
        "tblBorders": borders
    }

def parseCellProperties(tcPr: ET.Element, ns: dict) -> dict:
    w_el = tcPr.find("w:tcW", ns)
    tcW_type_raw = getAttr(w_el, "w:type", ns) if w_el is not None else None
    tcW = {
        "w": int(getAttr(w_el, "w:w", ns)) if getAttr(w_el, "w:w", ns) else None,
        "type": TableWidthType(tcW_type_raw) if tcW_type_raw is not None else None
    } if w_el is not None else None

    span_el = tcPr.find("w:gridSpan", ns)
    gridSpan = int(getAttr(span_el, "w:val", ns)) if span_el is not None else None

    v_align_el = tcPr.find("w:vAlign", ns)
    v_align_raw = getAttr(v_align_el, "w:val", ns) if v_align_el is not None else None
    vAlign = CellVAlign(v_align_raw) if v_align_raw is not None else None

    return {
        "tcW": tcW,
        "gridSpan": gridSpan,
        "vAlign": vAlign
    }

def parseTableStylePr(tblStylePr: ET.Element, ns: dict) -> dict:
    cond_type_raw = getAttr(tblStylePr, "w:type", ns)
    cond_type = TblStylePrType(cond_type_raw) if cond_type_raw is not None else None

    tbl_pr_el = tblStylePr.find("w:tblPr", ns)
    tc_pr_el = tblStylePr.find("w:tcPr", ns)

    return {
        "type": cond_type,
        "tblPr": parseTableProperties(tbl_pr_el, ns) if tbl_pr_el is not None else None,
        "tcPr": parseCellProperties(tc_pr_el, ns) if tc_pr_el is not None else None
    }
