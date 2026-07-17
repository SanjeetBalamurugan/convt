"""
 Copyright © 2026 Sanjeet Balamurugan. All rights reserved.
 This source code is licensed under the Orion License.
 Commercial use, commercialisation, and revenue generation are strictly prohibited.
 Personal, non-commercial use and modification are permitted.


 Any distributed modifications must attribute "Convt" and link to the homepage at "https://github.com/SanjeetBalamurugan/convt".
 See the root LICENSE file for details.
 """

PANOSE_DEFAULT = {
    "familyKind": "Unknown",
    "serifStyle": "Unknown",
    "weight": "Unknown",
    "proportion": "Unknown",
    "contrast": "Unknown",
    "strokeVariation": "Unknown",
    "armStyle": "Unknown",
    "letterform": "Unknown",
    "midline": "Unknown",
    "xHeight": "Unknown",
    "rawBytes": [0] * 10,
}

PANOSE_TABLES = {
  "familyKind" : {
    0: "Any", 1: "No Fit", 2: "Text and Display", 3: "Script", 4: "Decorative", 5: "Pictorial"
  },
  "serifStyle" : {
    0: "Any", 1: "No Fit", 2: "Cove", 3: "Obtuse Cove", 4: "Square Cove", 
    5: "Obtuse Square Cove", 6: "Square", 7: "Thin", 8: "Oval (Bone)", 
    9: "Exaggerated", 10: "Triangle", 11: "Normal Sans", 12: "Obtuse Sans", 
    13: "Perpendicular Sans", 14: "Flared", 15: "Rounded"
  },
  "weight": {
    0: "Any", 1: "No Fit", 2: "Very Light", 3: "Light", 4: "Thin", 
    5: "Book", 6: "Medium", 7: "Demi", 8: "Bold", 9: "Heavy", 
    10: "Black", 11: "Nord / Extra Black"
  },
  "proportion": {
    0: "Any", 1: "No Fit", 2: "Old Style", 3: "Modern", 4: "Even Width", 
    5: "Expanded", 6: "Condensed", 7: "Very Expanded", 8: "Very Condensed", 9: "Monospaced"
  },
  "contrast": {
    0: "Any", 1: "No Fit", 2: "None", 3: "Very Low", 4: "Low", 
    5: "Medium Low", 6: "Medium", 7: "Medium High", 8: "High", 9: "Very High"
  },
  "strokeVariation": {
    0: "Any", 1: "No Fit", 2: "No Variation", 3: "Gradual/Diagonal", 4: "Gradual/Transitional", 
    5: "Gradual/Vertical", 6: "Gradual/Horizontal", 7: "Rapid/Vertical", 8: "Rapid/Horizontal", 
    9: "Instant/Vertical"
  },
  "armStyle": {
    0: "Any", 1: "No Fit", 2: "Straight Arms/Horizontal", 3: "Straight Arms/Wedge", 4: "Straight Arms/Vertical", 
    5: "Straight Arms/Single Serif", 6: "Straight Arms/Double Serif", 7: "Non-Straight Arms/Horizontal", 
    8: "Non-Straight Arms/Wedge", 9: "Non-Straight Arms/Vertical", 10: "Non-Straight Arms/Single Serif", 
    11: "Non-Straight Arms/Double Serif"
  },
  "letterform": {
    0: "Any", 1: "No Fit", 2: "Normal/Contact", 3: "Normal/Weighted", 4: "Normal/Boxed", 
    5: "Normal/Flattened", 6: "Normal/Rounded", 7: "Normal/Off Center", 8: "Normal/Square", 
    9: "Oblique/Contact", 10: "Oblique/Weighted", 11: "Oblique/Boxed", 12: "Oblique/Flattened", 
    13: "Oblique/Rounded", 14: "Oblique/Off Center", 15: "Oblique/Square"
  },
  "midline": {
    0: "Any", 1: "No Fit", 2: "Standard/Trimmed", 3: "Standard/Pointed", 4: "Standard/Serifed", 
    5: "High/Trimmed", 6: "High/Pointed", 7: "High/Serifed", 8: "Constant/Trimmed", 
    9: "Constant/Pointed", 10: "Constant/Serifed", 11: "Low/Trimmed", 12: "Low/Pointed", 13: "Low/Serifed"
  },
  "xHeight": {
    0: "Any", 1: "No Fit", 2: "Constant/Small", 3: "Constant/Standard", 4: "Constant/Large", 
    5: "Ducking/Small", 6: "Ducking/Standard", 7: "Ducking/Large"
  }
};

def decodePanose(panose: str) -> dict:
    """
    Decodes a 10-byte PANOSE hex string into readable traits.
    Example Panose: 02020603050405020304    
    """
    PANOSE_LENGTH = 20

    if len(panose) != PANOSE_LENGTH:
        raise ValueError("Invalid PANOSE string. Must be a 10-byte hex sequence.")

    bytes_list = [int(panose[i:i+2], 16) for i in range(0, PANOSE_LENGTH, 2)]
    
    return {
        "familyKind": PANOSE_TABLES["familyKind"].get(bytes_list[0], "Unknown"),
        "serifStyle": PANOSE_TABLES["serifStyle"].get(bytes_list[1], "Unknown"),
        "weight": PANOSE_TABLES["weight"].get(bytes_list[2], "Unknown"),
        "proportion": PANOSE_TABLES["proportion"].get(bytes_list[3], "Unknown"),
        "contrast": PANOSE_TABLES["contrast"].get(bytes_list[4], "Unknown"),
        "strokeVariation": PANOSE_TABLES["strokeVariation"].get(
            bytes_list[5], "Unknown"
        ),
        "armStyle": PANOSE_TABLES["armStyle"].get(bytes_list[6], "Unknown"),
        "letterform": PANOSE_TABLES["letterform"].get(bytes_list[7], "Unknown"),
        "midline": PANOSE_TABLES["midline"].get(bytes_list[8], "Unknown"),
        "xHeight": PANOSE_TABLES["xHeight"].get(bytes_list[9], "Unknown"),
        "rawBytes": bytes_list,
    }