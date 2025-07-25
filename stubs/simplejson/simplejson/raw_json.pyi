"""Implementation of RawJSON"""

class RawJSON:
    """Wrap an encoded JSON document for direct embedding in the output"""

    encoded_json: str
    def __init__(self, encoded_json: str) -> None: ...
