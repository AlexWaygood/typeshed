from xml.etree.ElementTree import _FileRead

from openpyxl.cell.rich_text import CellRichText

def read_string_table(xml_source: _FileRead) -> list[str]:
    """Read in all shared strings in the table"""

def read_rich_text(xml_source: _FileRead) -> list[CellRichText | str]:
    """Read in all shared strings in the table"""
