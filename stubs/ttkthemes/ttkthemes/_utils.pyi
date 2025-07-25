"""
Author: RedFantom
License: GNU GPLv3
Copyright (c) 2017-2018 RedFantom
"""

from _typeshed import FileDescriptorOrPath, StrOrBytesPath
from contextlib import AbstractContextManager

def temporary_chdir(new_dir: FileDescriptorOrPath) -> AbstractContextManager[None]:
    """
    Like os.chdir(), but always restores the old working directory

    For example, code like this...

        old_curdir = os.getcwd()
        os.chdir('stuff')
        do_some_stuff()
        os.chdir(old_curdir)

    ...leaves the current working directory unchanged if do_some_stuff()
    raises an error, so it should be rewritten like this:

        old_curdir = os.getcwd()
        os.chdir('stuff')
        try:
            do_some_stuff()
        finally:
            os.chdir(old_curdir)

    Or equivalently, like this:

        with utils.temporary_chdir('stuff'):
            do_some_stuff()
    """

def get_file_directory() -> str:
    """Return an absolute path to the current file directory"""

def get_temp_directory() -> str:
    """Return an absolute path to an existing temporary directory"""

def get_themes_directory(theme_name: str | None = None, png: bool = False) -> str:
    """Return an absolute path the to /themes directory"""

def create_directory(directory: StrOrBytesPath) -> StrOrBytesPath:
    """Create directory but first delete it if it exists"""
