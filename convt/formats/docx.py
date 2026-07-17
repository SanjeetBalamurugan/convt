from enum import Enum
from zipfile import ZipFile

from convt.formats.docxdata.csb import CodePageBit0, CodePageBit1
from convt.formats.docxdata.panose import PANOSE_DEFAULT, decodePanose
from convt.formats.docxdata.usb import UnicodeSubrange0, UnicodeSubrange1, UnicodeSubrange2, UnicodeSubrange3
from convt.parser.hxml import getAttr, getNameSpaces

import xml.etree.ElementTree as ET

class WordCharset(Enum):
    """Hexadecimal w:charset values for OOXML fontTable.xml."""

    ANSI = "00"  # Windows ANSI / Western European
    DEFAULT = "01"  # System default locale / ANSI
    SYMBOL = "02"  # Special symbols and math characters
    MAC = "4D"  # Macintosh character set
    OEM = "77"  # IBM PC / Original Equipment Manufacturer
    SHIFTJIS = "80"  # Japanese (Shift-JIS)
    HANGUL = "81"  # Korean (Wansung/Johab)
    JOHAB = "82"  # Korean (Johab specific)
    GB2312 = "86"  # Simplified Chinese (GB2312)
    CHINESEBIG5 = "88"  # Traditional Chinese (Big5)
    GREEK = "A1"  # Greek
    TURKISH = "A2"  # Turkish
    VIETNAMESE = "A3"  # Vietnamese
    HEBREW = "B1"  # Hebrew
    ARABIC = "B2"  # Arabic
    BALTIC = "BA"  # Baltic
    RUSSIAN = "EE"  # Russian / Cyrillic
    THAI = "FE"  # Thai
    EASTEUROPE = "FF"  # Eastern European languages

class WordPitch(Enum): # Spacing Type
    VARIABLE = "variable"
    FIXED = "fixed"

def parseFontData(font: ET.Element[str], ns: dict) -> dict:
    fontName = getAttr(font, 'w:name', ns)
    fontFamily = getAttr(font.find("w:family", ns), "w:val", ns)
    charset = WordCharset(getAttr(font.find("w:charset", ns), "w:val", ns))
    panoseVal = getAttr(font.find("w:panose1", ns), "w:val", ns)
    panose = decodePanose(panoseVal) if panoseVal is not None else PANOSE_DEFAULT
    pitch = WordPitch(getAttr(font.find("w:pitch", ns), "w:val", ns))
    
    c0_data = getAttr(font.find("w:sig", ns), "w:csb0", ns)
    csb0 = CodePageBit0.parse_hex_mask(c0_data) if c0_data is not None else None

    c1_data = getAttr(font.find("w:sig", ns), "w:csb1", ns)
    csb1 = CodePageBit1.parse_hex_mask(c1_data) if c1_data is not None else None

    u0_data = getAttr(font.find("w:sig", ns), "w:usb0", ns)
    usb0 = UnicodeSubrange0.parse_hex_mask(u0_data) if u0_data is not None else None

    u1_data = getAttr(font.find("w:sig", ns), "w:usb1", ns)
    usb1 = UnicodeSubrange1.parse_hex_mask(u1_data) if u1_data is not None else None

    u2_data = getAttr(font.find("w:sig", ns), "w:usb2", ns)
    usb2 = UnicodeSubrange2.parse_hex_mask(u2_data) if u2_data is not None else None

    u3_data = getAttr(font.find("w:sig", ns), "w:usb3", ns)
    usb3 = UnicodeSubrange3.parse_hex_mask(u3_data) if u3_data is not None else None

    # TODO: ALTNAME needed?

    return {
        "fontName" : fontName,
        "fontFamily": fontFamily,

        "charset": charset,
        "panose1": panose,
        "pitch": pitch,

        "csb0": csb0,
        "csb1": csb1,

        "usb0": usb0,
        "usb1": usb1,
        "usb2": usb2,
        "usb3": usb3
    }

def extractFonts(document_path: str) -> dict:
    fontFilePath = "word/fontTable.xml"
    fonts = {}

    with ZipFile(document_path, "r") as zfile:
        fileList = zfile.namelist()
        
        if not fontFilePath in fileList:
            return {}
        

        with zfile.open(fontFilePath) as fontFile:
            content = fontFile.read().decode("utf-8")
            root = ET.fromstring(content)
            namespaces = getNameSpaces(content)

            for font in root.findall("w:font", namespaces):
                parsed = parseFontData(font, namespaces)
                fontName = parsed["fontName"]

                fonts[fontName] = parsed
    
    return fonts