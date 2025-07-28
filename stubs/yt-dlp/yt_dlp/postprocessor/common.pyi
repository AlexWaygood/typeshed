from _typeshed import StrPath
from collections.abc import Callable
from typing import Any

from ..extractor.common import _InfoDict
from ..YoutubeDL import YoutubeDL

class PostProcessorMetaClass(type):
    @staticmethod
    def run_wrapper(func: Callable[..., object]) -> Callable[..., object]: ...
    def __new__(cls, name: str, bases: tuple[type[Any], ...], attrs: dict[str, Any]) -> type[Any]: ...

class PostProcessor(metaclass=PostProcessorMetaClass):
    """Post Processor class.

    PostProcessor objects can be added to downloaders with their
    add_post_processor() method. When the downloader has finished a
    successful download, it will take its internal chain of PostProcessors
    and start calling the run() method on each one of them, first with
    an initial argument and then with the returned value of the previous
    PostProcessor.

    PostProcessor objects follow a "mutual registration" process similar
    to InfoExtractor objects.

    Optionally PostProcessor can use a list of additional command-line arguments
    with self._configuration_args.
    """

    PP_NAME: str
    def __init__(self, downloader: YoutubeDL | None = None) -> None: ...
    @classmethod
    def pp_key(cls) -> str: ...
    def to_screen(
        self,
        text: str,
        prefix: bool = True,
        *,
        message: str,
        skip_eol: bool = False,
        quiet: bool | None = None,
        only_once: bool = False,
    ) -> None: ...
    def report_warning(self, text: str, only_once: bool = False) -> None: ...
    def deprecation_warning(self, msg: str) -> None: ...
    def deprecated_feature(self, msg: str) -> None: ...
    def write_debug(self, text: str, *, only_once: bool = False) -> None: ...
    # *args and **kwargs are passed to .param.get() where param is normally a dict but does not have to be.
    def get_param(self, name: str, default: Any = None, *args: Any, **kwargs: Any) -> Any: ...
    def set_downloader(self, downloader: YoutubeDL) -> None:
        """Sets the downloader for this PP."""

    def run(self, information: _InfoDict) -> tuple[list[str], _InfoDict]:
        """Run the PostProcessor.

        The "information" argument is a dictionary like the ones
        composed by InfoExtractors. The only difference is that this
        one has an extra field called "filepath" that points to the
        downloaded file.

        This method returns a tuple, the first element is a list of the files
        that can be deleted, and the second of which is the updated
        information.

        In addition, this method may raise a PostProcessingError
        exception if post processing fails.
        """

    def try_utime(self, path: StrPath, atime: int, mtime: int, errnote: str = "Cannot update utime of file") -> None: ...
    def add_progress_hook(self, ph: Callable[[str], object]) -> None: ...
    def report_progress(self, s: str) -> None: ...
