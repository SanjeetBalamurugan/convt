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
from datetime import datetime

def parseWordDate(date: str) -> datetime:
    """ ISO 8601 DateTime Layout """
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")

def toWordDate(date: datetime) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:%S%z")

def currentDateTimeISO8601() -> str:
    now = datetime.now().astimezone()
    return toWordDate(now)

def parseInsTrack(ins: ET.Element, ns: dict) -> dict:
    id_raw = getAttr(ins, "w:id", ns)
    change_id = int(id_raw) if id_raw is not None else None

    author = getAttr(ins, "w:author", ns)
    date = parseWordDate(getAttr(ins, "w:date", ns) or currentDateTimeISO8601())

    return {
        "id": change_id,
        "author": author,
        "date": date
    }

def parseStyles_numPr(numPr: ET.Element, ns: dict) -> dict:
    result = {}

    numId = int(getAttr(numPr.find("w:numId"), "w:val", ns) or 0)
    result["numId"] = { "val": numId }

    indentationLevel = int(getAttr(numPr.find("w:ilvl"), "w:val", ns) or 0)
    result["ilvl"] = { "val": indentationLevel }

    numberingChange = numPr.find("w:numberingChange", ns)
    if numberingChange:
        numberingChangeID = int(getAttr(numberingChange, "w:id", ns))
        numberingChangeAuthor = getAttr(numberingChange, "w:author", ns)
        numberingChangeDate = parseWordDate(getAttr(numberingChange, "w:date", ns) or currentDateTimeISO8601())
        numberingChangeOriginal = getAttr(numberingChange, "w:original", ns)
        result["numberingChange"] = { "id": numberingChangeID, "author": numberingChangeAuthor, 
                                     "date": numberingChangeDate, "original": numberingChangeOriginal }
    else:
        result["numberingChange"] = { "id": None, "author": None, "date": None, "original": None }

    insertion = numPr.find("w:ins", ns)
    result["ins"] = parseInsTrack(insertion, ns) if insertion is not None else { "id": None, "author": None, "date": None}

    return result
