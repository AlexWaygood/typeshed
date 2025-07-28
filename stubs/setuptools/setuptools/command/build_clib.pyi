from setuptools.dist import Distribution

from .._distutils.command import build_clib as orig

class build_clib(orig.build_clib):
    """
    Override the default build_clib behaviour to do the following:

    1. Implement a rudimentary timestamp-based dependency system
       so 'compile()' doesn't run every time.
    2. Add more keys to the 'build_info' dictionary:
        * obj_deps - specify dependencies for each object compiled.
                     this should be a dictionary mapping a key
                     with the source filename to a list of
                     dependencies. Use an empty string for global
                     dependencies.
        * cflags   - specify a list of additional flags to pass to
                     the compiler.
    """

    distribution: Distribution  # override distutils.dist.Distribution with setuptools.dist.Distribution

    def build_libraries(self, libraries) -> None: ...
