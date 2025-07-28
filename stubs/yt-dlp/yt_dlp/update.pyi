import functools
from dataclasses import dataclass

from yt_dlp.utils._utils import NO_DEFAULT
from yt_dlp.YoutubeDL import YoutubeDL

__all__ = ["Updater"]

@dataclass
class UpdateInfo:
    """
    Update target information

    Can be created by `query_update()` or manually.

    Attributes:
        tag                 The release tag that will be updated to. If from query_update,
                            the value is after API resolution and update spec processing.
                            The only property that is required.
        version             The actual numeric version (if available) of the binary to be updated to,
                            after API resolution and update spec processing. (default: None)
        requested_version   Numeric version of the binary being requested (if available),
                            after API resolution only. (default: None)
        commit              Commit hash (if available) of the binary to be updated to,
                            after API resolution and update spec processing. (default: None)
                            This value will only match the RELEASE_GIT_HEAD of prerelease builds.
        binary_name         Filename of the binary to be updated to. (default: current binary name)
        checksum            Expected checksum (if available) of the binary to be
                            updated to. (default: None)
    """

    tag: str
    version: str | None = ...
    requested_version: str | None = ...
    commit: str | None = ...
    binary_name: str | None = ...
    checksum: str | None = ...

class Updater:
    ydl: YoutubeDL
    requested_channel: str
    requested_tag: str | None
    requested_repo: str | None
    def __init__(self, ydl: YoutubeDL, target: str | None = None) -> None: ...
    @property
    def current_version(self) -> str:
        """Current version"""

    @property
    def current_commit(self) -> str:
        """Current commit hash"""

    def query_update(self, *, _output: bool = False) -> UpdateInfo | None:
        """Fetches info about the available update
        @returns   An `UpdateInfo` if there is an update available, else None
        """

    def update(self, update_info: type[NO_DEFAULT] | None | UpdateInfo = ...) -> bool | None:
        """Update yt-dlp executable to the latest version
        @param update_info  `UpdateInfo | None` as returned by query_update()
        """

    @functools.cached_property
    def filename(self) -> str:
        """Filename of the executable"""

    @functools.cached_property
    def cmd(self) -> list[str]:
        """The command-line to run the executable, if known"""

    def restart(self) -> int:
        """Restart the executable"""
