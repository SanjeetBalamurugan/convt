import io
import xml.etree.ElementTree as ET

def getNameSpaces(xml_data: str) -> dict:
    events = ET.iterparse(io.StringIO(xml_data), events=('start-ns',))
    out = {}

    for _, elem in events:
        prefix, url = elem
        out[prefix] = url

    return out

def getAttr(element: ET.Element[str], prefixed_attr: str, ns_map: dict):
    prefix, attr_name = prefixed_attr.split(':')
    url = ns_map[prefix]
    
    try:
        return element.get(f"{{{url}}}{attr_name}")
    except AttributeError: # Most Likely the element doesnt exist
        return None