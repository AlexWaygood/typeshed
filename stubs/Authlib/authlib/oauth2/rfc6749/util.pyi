from collections.abc import Collection

def list_to_scope(scope: Collection[str] | str | None) -> str:
    """Convert a list of scopes to a space separated string."""

def scope_to_list(scope: Collection[str] | str | None) -> list[str]:
    """Convert a space separated string to a list of scopes."""

def extract_basic_authorization(headers: dict[str, str]) -> tuple[str, str]: ...
