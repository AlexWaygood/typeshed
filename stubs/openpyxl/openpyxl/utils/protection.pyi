def hash_password(plaintext_password: str = "") -> str:
    """
    Create a password hash from a given string for protecting a worksheet
    only. This will not work for encrypting a workbook.

    This method is based on the algorithm provided by
    Daniel Rentz of OpenOffice and the PEAR package
    Spreadsheet_Excel_Writer by Xavier Noguer <xnoguer@rezebra.com>.
    See also http://blogs.msdn.com/b/ericwhite/archive/2008/02/23/the-legacy-hashing-algorithm-in-open-xml.aspx
    """
