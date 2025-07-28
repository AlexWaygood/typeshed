class DefaultDynamicNaming:
    """
    Decides what name to use on a segment generated from an incoming request.
    By default it takes the host name and compares it to a pre-defined pattern.
    If the host name matches that pattern, it returns the host name, otherwise
    it returns the fallback name. The host name usually comes from the incoming
    request's headers.
    """

    def __init__(self, pattern: str, fallback: str) -> None:
        """
        :param str pattern: the regex-like pattern to be compared against.
            Right now only ? and * are supported. An asterisk (*) represents
            any combination of characters. A question mark (?) represents
            any single character.
        :param str fallback: the fallback name to be used if the candidate name
            doesn't match the provided pattern.
        """

    def get_name(self, host_name: str | None) -> str:
        """
        Returns the segment name based on the input host name.
        """
