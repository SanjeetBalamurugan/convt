"""
 Copyright © 2026 Sanjeet Balamurugan. All rights reserved.
 This source code is licensed under the Orion License.
 Commercial use, commercialisation, and revenue generation are strictly prohibited.
 Personal, non-commercial use and modification are permitted.


 Any distributed modifications must attribute "Convt" and link to the homepage at "https://github.com/SanjeetBalamurugan/convt".
 See the root LICENSE file for details.
 """

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