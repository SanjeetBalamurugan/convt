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

def parseLsdException(lsd: ET.Element, ns: dict) -> dict:
    name = getAttr(lsd, "w:name", ns)
    
    ui_priority_raw = getAttr(lsd, "w:uiPriority", ns)
    ui_priority = int(ui_priority_raw) if ui_priority_raw is not None else None

    locked_raw = getAttr(lsd, "w:locked", ns)
    locked = locked_raw.lower() in ["1", "true"] if locked_raw else None

    semi_hidden_raw = getAttr(lsd, "w:semiHidden", ns)
    semi_hidden = semi_hidden_raw.lower() in ["1", "true"] if semi_hidden_raw else None

    unhide_raw = getAttr(lsd, "w:unhideWhenUsed", ns)
    unhide_when_used = unhide_raw.lower() in ["1", "true"] if unhide_raw else None

    q_format_raw = getAttr(lsd, "w:qFormat", ns)
    q_format = q_format_raw.lower() in ["1", "true"] if q_format_raw else None

    return {
        "name": name,
        "uiPriority": ui_priority,
        "locked": locked,
        "semiHidden": semi_hidden,
        "unhideWhenUsed": unhide_when_used,
        "qFormat": q_format
    }

def parseLatentStyles(latentStyles: ET.Element, ns: dict) -> dict:
    def_locked = getAttr(latentStyles, "w:defLockedState", ns)
    def_ui = getAttr(latentStyles, "w:defUIPriority", ns)
    def_semi = getAttr(latentStyles, "w:defSemiHidden", ns)
    def_unhide = getAttr(latentStyles, "w:defUnhideWhenUsed", ns)
    def_qf = getAttr(latentStyles, "w:defQFormat", ns)
    count_raw = getAttr(latentStyles, "w:count", ns)

    exceptions = latentStyles.findall("w:lsdException", ns)

    return {
        "defLockedState": def_locked.lower() in ["1", "true"] if def_locked else False,
        "defUIPriority": int(def_ui) if def_ui is not None else 99,
        "defSemiHidden": def_semi.lower() in ["1", "true"] if def_semi else False,
        "defUnhideWhenUsed": def_unhide.lower() in ["1", "true"] if def_unhide else False,
        "defQFormat": def_qf.lower() in ["1", "true"] if def_qf else False,
        "count": int(count_raw) if count_raw is not None else 0,
        "exceptions": [parseLsdException(el, ns) for el in exceptions]
    }
