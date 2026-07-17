"""
 Copyright © 2026 Sanjeet Balamurugan. All rights reserved.
 This source code is licensed under the Orion License.
 Commercial use, commercialisation, and revenue generation are strictly prohibited.
 Personal, non-commercial use and modification are permitted.


 Any distributed modifications must attribute "Convt" and link to the homepage at "https://github.com/SanjeetBalamurugan/convt".
 See the root LICENSE file for details.
 """

from enum import IntEnum


class UnicodeSubrange0(IntEnum):
    """32-bit flags for w:usb0 (Bits 0-31: Core Western & Global scripts)."""

    BASIC_LATIN = 0
    LATIN_1_SUPPLEMENT = 1
    LATIN_EXTENDED_A = 2
    LATIN_EXTENDED_B = 3
    IPA_EXTENSIONS = 4
    SPACING_MODIFIER_LETTERS = 5
    COMBINING_DIACRITICAL_MARKS = 6
    GREEK_AND_COPTIC = 7
    COPTIC = 8
    CYRILLIC = 9
    ARMENIAN = 10
    HEBREW = 11
    VAI = 12
    ARABIC = 13
    NKO = 14
    DEVANAGARI = 15
    BENGALI = 16
    GURMUKHI = 17
    GUJARATI = 18
    ORIYA = 19
    TAMIL = 20
    TELUGU = 21
    KANNADA = 22
    MALAYALAM = 23
    SINHALA = 24
    THAI = 25
    LAO = 26
    TIBETAN = 27
    MYANMAR = 28
    GEORGIAN = 29
    HANGUL_JAMO = 30
    ETHIOPIC = 31

    @classmethod
    def generate_hex_mask(cls, active_flags: list["UnicodeSubrange0"]) -> str:
        mask = 0
        for flag in active_flags:
            mask |= 1 << flag.value
        return f"{mask:08X}"

    @classmethod
    def parse_hex_mask(cls, hex_string: str) -> list["UnicodeSubrange0"]:
        mask = int(hex_string, 16)
        return [flag for flag in cls if (mask & (1 << flag.value))]


class UnicodeSubrange1(IntEnum):
    """32-bit flags for w:usb1 (Bits 32-63: Symbols, Extended Writing & Early CJK)."""

    CHEROKEE = 32
    UNIFIED_CANADIAN_ABORIGINAL_SYLLABICS = 33
    OGHAM = 34
    RUNIC = 35
    KHMER = 36
    MONGOLIAN = 37
    BRAILLE_PATTERNS = 38
    YI_SYLLABLES_AND_RADICALS = 39
    TAGALOG_HANUNOO_BUHID_TAGBANWA = 40
    OLD_ITALIC = 41
    GOTHIC = 42
    DESERET = 43
    MUSICAL_SYMBOLS = 44
    MATHEMATICAL_ALPHANUMERIC_SYMBOLS = 45
    PRIVATE_USE_AREA_RESERVED = 46
    CJK_RADICALS_SUPPLEMENT = 47
    CJK_SYMBOLS_AND_PUNCTUATION = 48
    ENCLOSED_CJK_LETTERS_AND_MONTHS = 49
    CJK_COMPATIBILITY = 50
    HANGUL_SYLLABLES = 51
    NON_PLANE_0_RESERVED = 52
    CJK_UNIFIED_IDEOGRAPHS = 53
    PRIVATE_USE_PLANE_15_AND_16 = 54
    CJK_COMPATIBILITY_IDEOGRAPHS = 55
    ALPHABETIC_PRESENTATION_FORMS = 56
    ARABIC_PRESENTATION_FORMS_A = 57
    COMBINING_HALF_MARKS = 58
    CJK_COMPATIBILITY_FORMS = 59
    SMALL_FORM_VARIANTS = 60
    ARABIC_PRESENTATION_FORMS_B = 61
    HALFWIDTH_AND_FULLWIDTH_FORMS = 62
    SPECIALS = 63

    @classmethod
    def generate_hex_mask(cls, active_flags: list["UnicodeSubrange1"]) -> str:
        mask = 0
        for flag in active_flags:
            mask |= 1 << (flag.value - 32)
        return f"{mask:08X}"

    @classmethod
    def parse_hex_mask(cls, hex_string: str) -> list["UnicodeSubrange1"]:
        mask = int(hex_string, 16)
        return [flag for flag in cls if (mask & (1 << (flag.value - 32)))]


class UnicodeSubrange2(IntEnum):
    """32-bit flags for w:usb2 (Bits 64-95: Extended punctuation, Symbols & Math)."""

    TIBETAN_RESERVED = 64
    PHAGS_PA = 65
    LIMBU = 66
    TAI_LE = 67
    NEW_TAI_LUE = 68
    BUGINESE = 69
    GLAGOLITIC = 70
    TIFINAGH = 71
    YIJING_HEXAGRAM_SYMBOLS = 72
    SYRIAC = 73
    THAANA = 74
    LINEAR_B_SYLLABARY_AND_IDEOGRAMS = 75
    AEGEAN_NUMBERS = 76
    UGARITIC = 77
    OLD_PERSIAN = 78
    PHOENICIAN = 79
    KHAROSHTHI = 80
    KHAROSHTHI_RESERVED = 81
    LEPCHA = 82
    OL_CHIKI = 83
    SAURASHTRA = 84
    KAYAH_LI = 85
    REJANG = 86
    CHAM = 87
    ANCIENT_SYMBOLS = 88
    PHAISTOS_DISK = 89
    CARIAN_LYCIAN_LYDIAN = 90
    DOMINO_AND_MAHJONG_TILES = 91
    HISTORICAL_RESERVED_92 = 92
    HISTORICAL_RESERVED_93 = 93
    HISTORICAL_RESERVED_94 = 94
    HISTORICAL_RESERVED_95 = 95

    @classmethod
    def generate_hex_mask(cls, active_flags: list["UnicodeSubrange2"]) -> str:
        mask = 0
        for flag in active_flags:
            mask |= 1 << (flag.value - 64)
        return f"{mask:08X}"

    @classmethod
    def parse_hex_mask(cls, hex_string: str) -> list["UnicodeSubrange2"]:
        mask = int(hex_string, 16)
        return [flag for flag in cls if (mask & (1 << (flag.value - 64)))]


class UnicodeSubrange3(IntEnum):
    """32-bit flags for w:usb3 (Bits 96-127: Modern Additions & System Variances)."""

    GENERAL_PUNCTUATION = 96
    SUPERSCRIPTS_AND_SUBSCRIPTS = 97
    CURRENCY_SYMBOLS = 98
    COMBINING_DIACRITICAL_MARKS_FOR_SYMBOLS = 99
    LETTERLIKE_SYMBOLS = 100
    NUMBER_FORMS = 101
    ARROWS = 102
    MATHEMATICAL_OPERATORS = 103
    MISCELLANEOUS_TECHNICAL = 104
    CONTROL_PICTURES = 105
    OPTICAL_CHARACTER_RECOGNITION = 106
    ENCLOSED_ALPHANUMERICS = 107
    BOX_DRAWING = 108
    BLOCK_ELEMENTS = 109
    GEOMETRIC_SHAPES = 110
    MISCELLANEOUS_SYMBOLS = 111
    DINGBATS = 112
    CJK_COMPATIBILITY_IDEOGRAPHS_SUPPLEMENT = 113
    TAGS = 114
    VARIATION_SELECTORS = 115
    RESERVED_BIT_116 = 116
    RESERVED_BIT_117 = 117
    RESERVED_BIT_118 = 118
    RESERVED_BIT_119 = 119
    RESERVED_BIT_120 = 120
    RESERVED_BIT_121 = 121
    RESERVED_BIT_122 = 122
    RESERVED_BIT_123 = 123
    RESERVED_BIT_124 = 124
    RESERVED_BIT_125 = 125
    RESERVED_BIT_126 = 126
    RESERVED_BIT_127 = 127

    @classmethod
    def generate_hex_mask(cls, active_flags: list["UnicodeSubrange3"]) -> str:
        mask = 0
        for flag in active_flags:
            mask |= 1 << (flag.value - 96)
        return f"{mask:08X}"

    @classmethod
    def parse_hex_mask(cls, hex_string: str) -> list["UnicodeSubrange3"]:
        mask = int(hex_string, 16)
        return [flag for flag in cls if (mask & (1 << (flag.value - 96)))]
