from enum import IntEnum


class CodePageBit0(IntEnum):
    """32-bit boolean flags for the w:csb0 attribute in OOXML fontTable.xml."""

    LATIN_2_CENTRAL_EUROPE = 0  # Windows 1250
    CYRILLIC = 1  # Windows 1251
    LATIN_1_WESTERN_EUROPE = 2  # Windows 1252
    GREEK = 3  # Windows 1253
    TURKISH = 4  # Windows 1254
    HEBREW = 5  # Windows 1255
    ARABIC = 6  # Windows 1256
    BALTIC = 7  # Windows 1257
    VIETNAMESE = 8  # Windows 1258

    # Bits 9-15 are reserved by Microsoft (Always 0)

    JAPANESE_SHIFT_JIS = 16  # Windows 932
    SIMPLIFIED_CHINESE_GB2312 = 17  # Windows 936
    KOREAN_WANSUNG = 18  # Windows 949
    TRADITIONAL_CHINESE_BIG5 = 19  # Windows 950
    KOREAN_JOHAB = 20  # Windows 1361

    # Bits 21-28 are reserved by Microsoft (Always 0)

    MACINTOSH_ROMAN = 29  # Legacy Mac Roman Character Set
    ADOBE_OEM = 30  # Adobe OEM Character Set
    SYMBOL = 31  # Symbol Character Set (Math/Symbols)

    @classmethod
    def generate_hex_mask(cls, active_flags: list["CodePageBit0"]) -> str:
        """Generates the 8-character uppercase hex string for w:csb0."""
        mask = 0
        for flag in active_flags:
            mask |= 1 << flag.value
        return f"{mask:08X}"

    @classmethod
    def parse_hex_mask(cls, hex_string: str) -> list["CodePageBit0"]:
        """Parses a w:csb0 hex string back into a list of active Enum flags."""
        mask = int(hex_string, 16)
        return [flag for flag in cls if (mask & (1 << flag.value))]
    
class CodePageBit1(IntEnum):
    """32-bit boolean flags for the w:csb1 attribute (Bits 32-63 of OpenType code pages)."""

    # Legacy Macintosh Character Sets
    MAC_ROMAN_RESERVED = 32  # Bit 0 of csb1
    MAC_JAPANESE = 33  # Bit 1 of csb1
    MAC_TRADITIONAL_CHINESE = 34  # Bit 2 of csb1
    MAC_KOREAN = 35  # Bit 3 of csb1
    MAC_ARABIC = 36  # Bit 4 of csb1
    MAC_HEBREW = 37  # Bit 5 of csb1
    MAC_GREEK = 38  # Bit 6 of csb1
    MAC_CYRILLIC = 39  # Bit 7 of csb1
    MAC_RUSSIAN = 40  # Bit 8 of csb1
    MAC_ROMANIAN = 41  # Bit 9 of csb1
    MAC_UKRAINIAN = 42  # Bit 10 of csb1
    MAC_THAI = 43  # Bit 11 of csb1
    MAC_SIMPLIFIED_CHINESE = 44  # Bit 12 of csb1

    # Legacy MS-DOS / IBM OEM Console Code Pages
    OEM_858_EURO = 48  # Bit 16 of csb1 (IBM OEM Latin 1 with Euro sign)
    OEM_869_GREEK = 49  # Bit 17 of csb1
    OEM_866_CYRILLIC = 50  # Bit 18 of csb1 (MS-DOS Russian)
    OEM_865_NORDIC = 51  # Bit 19 of csb1
    OEM_864_ARABIC = 52  # Bit 20 of csb1
    OEM_863_CANADIAN_FRENCH = 53  # Bit 21 of csb1
    OEM_862_HEBREW = 54  # Bit 22 of csb1
    OEM_861_ICELANDIC = 55  # Bit 23 of csb1
    OEM_860_PORTUGUESE = 56  # Bit 24 of csb1
    OEM_857_TURKISH = 57  # Bit 25 of csb1
    OEM_855_CYRILLIC = 58  # Bit 26 of csb1
    OEM_852_LATIN_2 = 59  # Bit 27 of csb1 (MS-DOS Slavic/Central Europe)
    OEM_775_BALTIC = 60  # Bit 28 of csb1
    OEM_737_GREEK = 61  # Bit 29 of csb1
    OEM_850_MULTILINGUAL_LATIN_1 = 62  # Bit 30 of csb1 (Classic DOS Western Europe)
    OEM_437_US_IBM_PC = 63  # Bit 31 of csb1 (The Original IBM PC code page)

    @classmethod
    def generate_hex_mask(cls, active_flags: list["CodePageBit1"]) -> str:
        """Generates the 8-character uppercase hex string for w:csb1."""
        mask = 0
        for flag in active_flags:
            # Shift value must normalize down to a 0-31 byte slot index
            normalized_bit = flag.value - 32
            mask |= 1 << normalized_bit
        return f"{mask:08X}"

    @classmethod
    def parse_hex_mask(cls, hex_string: str) -> list["CodePageBit1"]:
        """Parses a w:csb1 hex string back into a list of active Enum flags."""
        mask = int(hex_string, 16)
        return [
            flag for flag in cls if (mask & (1 << (flag.value - 32)))
        ]