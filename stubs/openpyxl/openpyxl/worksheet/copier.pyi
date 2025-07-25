from openpyxl.worksheet.worksheet import Worksheet

class WorksheetCopy:
    """
    Copy the values, styles, dimensions, merged cells, margins, and
    print/page setup from one worksheet to another within the same
    workbook.
    """

    source: Worksheet
    target: Worksheet
    def __init__(self, source_worksheet: Worksheet, target_worksheet: Worksheet) -> None: ...
    def copy_worksheet(self) -> None: ...
