"""
The crontabs manager will list all available crontabs on the system.
"""

from typing import Any

from crontab import CronTab

class UserSpool(list[CronTab]):
    """Generates all user crontabs, yields both owned and abandoned tabs"""

    def __init__(self, loc: str, tabs: CronTabs | None = ...) -> None: ...
    def listdir(self, loc: str) -> list[str]: ...
    def get_owner(self, path: str) -> str:
        """Returns user file at path"""

    def generate(self, loc: str, username: str) -> CronTab: ...

class SystemTab(list[CronTab]):
    """Generates all system tabs"""

    def __init__(self, loc: str, tabs: CronTabs | None = ...) -> None: ...

class AnaCronTab(list[CronTab]):
    """Attempts to digest anacron entries (if possible)"""

    def __init__(self, loc: str, tabs: CronTabs | None = ...) -> None: ...
    def add(self, loc: str, item: str, anajob: CronTab) -> CronTab: ...

KNOWN_LOCATIONS: list[tuple[UserSpool | SystemTab | AnaCronTab, str]]

class CronTabs(list[UserSpool | SystemTab | AnaCronTab]):
    """Singleton dictionary of all detectable crontabs"""

    def __init__(self) -> None: ...
    def add(self, cls: type[UserSpool | SystemTab | AnaCronTab], *args: Any) -> None: ...
    @property
    def all(self) -> CronTab:
        """Return a CronTab object with all jobs (read-only)"""
