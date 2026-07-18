"""
 Copyright © 2026 Sanjeet Balamurugan. All rights reserved.
 This source code is licensed under the Orion License.
 Commercial use, commercialisation, and revenue generation are strictly prohibited.
 Personal, non-commercial use and modification are permitted.


 Any distributed modifications must attribute "Convt" and link to the homepage at "https://github.com/SanjeetBalamurugan/convt".
 See the root LICENSE file for details.
 """

from enum import StrEnum


class SystemColorVal(StrEnum):
    WINDOW_TEXT = "windowText"
    WINDOW = "window"

class ThemeColorElement(StrEnum):
    DK1 = "dk1"
    LT1 = "lt1"
    DK2 = "dk2"
    LT2 = "lt2"
    ACCENT1 = "accent1"
    ACCENT2 = "accent2"
    ACCENT3 = "accent3"
    ACCENT4 = "accent4"
    ACCENT5 = "accent5"
    ACCENT6 = "accent6"
    HLINK = "hlink"
    FOL_HLINK = "folHlink"