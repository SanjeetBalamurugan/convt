from enum import StrEnum

class AsciiTheme(StrEnum):
    MAJORASCII = "majorAscii"
    MINORASCII = "minorAscii"
    MAJORHANSI = "majorHAnsi"
    MINORHANSI = "minorHAnsi"
    MAJORBIDI = "majorBidi"
    MINORBIDI = "minorBidi"

EastAsiaTheme = StrEnum(
    "EastAsiaTheme",
    {
        **{m.name:m.value for m in AsciiTheme},
        "MAJOREASTASIA" : "majorEastAsia",
        "MINOREASTASIA" : "minorEastAsia"
    }
)

class RFontHint(StrEnum):
    DEFAULT = "default"
    EASTASIA = "eastAsia"
    CS = "cs"