from .common import InfoExtractor

def gen_extractor_classes() -> list[type[InfoExtractor]]:
    """Return a list of supported extractors.
    The order does matter; the first extractor matched is the one handling the URL.
    """

def gen_extractors() -> list[InfoExtractor]:
    """Return a list of an instance of every supported extractor.
    The order does matter; the first extractor matched is the one handling the URL.
    """

def list_extractor_classes(age_limit: int | None = None) -> list[type[InfoExtractor]]:
    """Return a list of extractors that are suitable for the given age, sorted by extractor name"""

def list_extractors(age_limit: int | None = None) -> list[InfoExtractor]:
    """Return a list of extractor instances that are suitable for the given age, sorted by extractor name"""

def get_info_extractor(ie_name: str) -> InfoExtractor:
    """Returns the info extractor class with the given ie_name"""

def import_extractors() -> None: ...
