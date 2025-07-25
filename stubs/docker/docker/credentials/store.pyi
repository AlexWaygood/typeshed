from _typeshed import Incomplete

class Store:
    program: Incomplete
    exe: Incomplete
    environment: Incomplete
    def __init__(self, program, environment=None) -> None:
        """Create a store object that acts as an interface to
        perform the basic operations for storing, retrieving
        and erasing credentials using `program`.
        """

    def get(self, server):
        """Retrieve credentials for `server`. If no credentials are found,
        a `StoreError` will be raised.
        """

    def store(self, server, username, secret):
        """Store credentials for `server`. Raises a `StoreError` if an error
        occurs.
        """

    def erase(self, server) -> None:
        """Erase credentials for `server`. Raises a `StoreError` if an error
        occurs.
        """

    def list(self):
        """List stored credentials. Requires v0.4.0+ of the helper."""
