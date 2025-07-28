from _typeshed import Incomplete

class PaginatedResult:
    """
    An instance of this class is returned from paginated operations
    """

    total_items: Incomplete
    page_size: Incomplete
    current_page: Incomplete
    def __init__(self, total_items, page_size, current_page) -> None: ...
