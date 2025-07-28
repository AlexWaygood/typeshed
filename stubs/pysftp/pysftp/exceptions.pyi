"""pysftp specific exceptions"""

class ConnectionException(Exception):
    """Exception raised for connection problems

    Attributes:
        message  -- explanation of the error
    """

    message: str
    def __init__(self, host: str, port: int) -> None: ...

class CredentialException(Exception):
    """Exception raised for credential problems

    Attributes:
        message  -- explanation of the error
    """

    message: str
    def __init__(self, message: str) -> None: ...

class HostKeysException(Exception):
    """raised when a problem with HostKeys is encountered"""
