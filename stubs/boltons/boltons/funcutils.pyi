"""Python's built-in :mod:`functools` module builds several useful
utilities on top of Python's first-class function
support. ``funcutils`` generally stays in the same vein, adding to and
correcting Python's standard metaprogramming facilities.
"""

import functools
from _typeshed import Incomplete
from functools import total_ordering as total_ordering

NO_DEFAULT: Incomplete

def inspect_formatargspec(
    args,
    varargs=None,
    varkw=None,
    defaults=None,
    kwonlyargs=(),
    kwonlydefaults={},
    annotations={},
    formatarg=...,
    formatvarargs=...,
    formatvarkw=...,
    formatvalue=...,
    formatreturns=...,
    formatannotation=...,
):
    """Copy formatargspec from python 3.7 standard library.
    Python 3 has deprecated formatargspec and requested that Signature
    be used instead, however this requires a full reimplementation
    of formatargspec() in terms of creating Parameter objects and such.
    Instead of introducing all the object-creation overhead and having
    to reinvent from scratch, just copy their compatibility routine.
    """

def get_module_callables(mod, ignore=None):
    """Returns two maps of (*types*, *funcs*) from *mod*, optionally
    ignoring based on the :class:`bool` return value of the *ignore*
    callable. *mod* can be a string name of a module in
    :data:`sys.modules` or the module instance itself.
    """

def mro_items(type_obj):
    """Takes a type and returns an iterator over all class variables
    throughout the type hierarchy (respecting the MRO).

    >>> sorted(set([k for k, v in mro_items(int) if not k.startswith('__') and 'bytes' not in k and not callable(v)]))
    ['denominator', 'imag', 'numerator', 'real']
    """

def dir_dict(obj, raise_exc: bool = False):
    """Return a dictionary of attribute names to values for a given
    object. Unlike ``obj.__dict__``, this function returns all
    attributes on the object, including ones on parent classes.
    """

def copy_function(orig, copy_dict: bool = True):
    """Returns a shallow copy of the function, including code object,
    globals, closure, etc.

    >>> func = lambda: func
    >>> func() is func
    True
    >>> func_copy = copy_function(func)
    >>> func_copy() is func
    True
    >>> func_copy is not func
    True

    Args:
        orig (function): The function to be copied. Must be a
            function, not just any method or callable.
        copy_dict (bool): Also copy any attributes set on the function
            instance. Defaults to ``True``.
    """

def partial_ordering(cls):
    """Class decorator, similar to :func:`functools.total_ordering`,
    except it is used to define `partial orderings`_ (i.e., it is
    possible that *x* is neither greater than, equal to, or less than
    *y*). It assumes the presence of the ``__le__()`` and ``__ge__()``
    method, but nothing else. It will not override any existing
    additional comparison methods.

    .. _partial orderings: https://en.wikipedia.org/wiki/Partially_ordered_set

    >>> @partial_ordering
    ... class MySet(set):
    ...     def __le__(self, other):
    ...         return self.issubset(other)
    ...     def __ge__(self, other):
    ...         return self.issuperset(other)
    ...
    >>> a = MySet([1,2,3])
    >>> b = MySet([1,2])
    >>> c = MySet([1,2,4])
    >>> b < a
    True
    >>> b > a
    False
    >>> b < c
    True
    >>> a < c
    False
    >>> c > a
    False
    """

class InstancePartial(functools.partial[Incomplete]):
    """:class:`functools.partial` is a huge convenience for anyone
    working with Python's great first-class functions. It allows
    developers to curry arguments and incrementally create simpler
    callables for a variety of use cases.

    Unfortunately there's one big gap in its usefulness:
    methods. Partials just don't get bound as methods and
    automatically handed a reference to ``self``. The
    ``InstancePartial`` type remedies this by inheriting from
    :class:`functools.partial` and implementing the necessary
    descriptor protocol. There are no other differences in
    implementation or usage. :class:`CachedInstancePartial`, below,
    has the same ability, but is slightly more efficient.

    """

    def __get__(self, obj, obj_type): ...

class CachedInstancePartial(functools.partial[Incomplete]):
    """The ``CachedInstancePartial`` is virtually the same as
    :class:`InstancePartial`, adding support for method-usage to
    :class:`functools.partial`, except that upon first access, it
    caches the bound method on the associated object, speeding it up
    for future accesses, and bringing the method call overhead to
    about the same as non-``partial`` methods.

    See the :class:`InstancePartial` docstring for more details.
    """

    __name__: Incomplete
    def __set_name__(self, obj_type, name) -> None: ...
    __doc__: Incomplete
    __module__: Incomplete
    def __get__(self, obj, obj_type): ...

partial = CachedInstancePartial

def format_invocation(name: str = "", args=(), kwargs=None, **kw):
    """Given a name, positional arguments, and keyword arguments, format
    a basic Python-style function call.

    >>> print(format_invocation('func', args=(1, 2), kwargs={'c': 3}))
    func(1, 2, c=3)
    >>> print(format_invocation('a_func', args=(1,)))
    a_func(1)
    >>> print(format_invocation('kw_func', kwargs=[('a', 1), ('b', 2)]))
    kw_func(a=1, b=2)

    """

def format_exp_repr(obj, pos_names, req_names=None, opt_names=None, opt_key=None):
    """Render an expression-style repr of an object, based on attribute
    names, which are assumed to line up with arguments to an initializer.

    >>> class Flag(object):
    ...    def __init__(self, length, width, depth=None):
    ...        self.length = length
    ...        self.width = width
    ...        self.depth = depth
    ...

    That's our Flag object, here are some example reprs for it:

    >>> flag = Flag(5, 10)
    >>> print(format_exp_repr(flag, ['length', 'width'], [], ['depth']))
    Flag(5, 10)
    >>> flag2 = Flag(5, 15, 2)
    >>> print(format_exp_repr(flag2, ['length'], ['width', 'depth']))
    Flag(5, width=15, depth=2)

    By picking the pos_names, req_names, opt_names, and opt_key, you
    can fine-tune how you want the repr to look.

    Args:
       obj (object): The object whose type name will be used and
          attributes will be checked
       pos_names (list): Required list of attribute names which will be
          rendered as positional arguments in the output repr.
       req_names (list): List of attribute names which will always
          appear in the keyword arguments in the output repr. Defaults to None.
       opt_names (list): List of attribute names which may appear in
          the keyword arguments in the output repr, provided they pass
          the *opt_key* check. Defaults to None.
       opt_key (callable): A function or callable which checks whether
          an opt_name should be in the repr. Defaults to a
          ``None``-check.

    """

def format_nonexp_repr(obj, req_names=None, opt_names=None, opt_key=None):
    """Format a non-expression-style repr

    Some object reprs look like object instantiation, e.g., App(r=[], mw=[]).

    This makes sense for smaller, lower-level objects whose state
    roundtrips. But a lot of objects contain values that don't
    roundtrip, like types and functions.

    For those objects, there is the non-expression style repr, which
    mimic's Python's default style to make a repr like so:

    >>> class Flag(object):
    ...    def __init__(self, length, width, depth=None):
    ...        self.length = length
    ...        self.width = width
    ...        self.depth = depth
    ...
    >>> flag = Flag(5, 10)
    >>> print(format_nonexp_repr(flag, ['length', 'width'], ['depth']))
    <Flag length=5 width=10>

    If no attributes are specified or set, utilizes the id, not unlike Python's
    built-in behavior.

    >>> print(format_nonexp_repr(flag))
    <Flag id=...>
    """

def wraps(func, injected=None, expected=None, **kw):
    """Decorator factory to apply update_wrapper() to a wrapper function.

    Modeled after built-in :func:`functools.wraps`. Returns a decorator
    that invokes update_wrapper() with the decorated function as the wrapper
    argument and the arguments to wraps() as the remaining arguments.
    Default arguments are as for update_wrapper(). This is a convenience
    function to simplify applying partial() to update_wrapper().

    Same example as in update_wrapper's doc but with wraps:

        >>> from boltons.funcutils import wraps
        >>>
        >>> def print_return(func):
        ...     @wraps(func)
        ...     def wrapper(*args, **kwargs):
        ...         ret = func(*args, **kwargs)
        ...         print(ret)
        ...         return ret
        ...     return wrapper
        ...
        >>> @print_return
        ... def example():
        ...     '''docstring'''
        ...     return 'example return value'
        >>>
        >>> val = example()
        example return value
        >>> example.__name__
        'example'
        >>> example.__doc__
        'docstring'
    """

def update_wrapper(wrapper, func, injected=None, expected=None, build_from=None, **kw):
    """Modeled after the built-in :func:`functools.update_wrapper`,
    this function is used to make your wrapper function reflect the
    wrapped function's:

      * Name
      * Documentation
      * Module
      * Signature

    The built-in :func:`functools.update_wrapper` copies the first three, but
    does not copy the signature. This version of ``update_wrapper`` can copy
    the inner function's signature exactly, allowing seamless usage
    and :mod:`introspection <inspect>`. Usage is identical to the
    built-in version::

        >>> from boltons.funcutils import update_wrapper
        >>>
        >>> def print_return(func):
        ...     def wrapper(*args, **kwargs):
        ...         ret = func(*args, **kwargs)
        ...         print(ret)
        ...         return ret
        ...     return update_wrapper(wrapper, func)
        ...
        >>> @print_return
        ... def example():
        ...     '''docstring'''
        ...     return 'example return value'
        >>>
        >>> val = example()
        example return value
        >>> example.__name__
        'example'
        >>> example.__doc__
        'docstring'

    In addition, the boltons version of update_wrapper supports
    modifying the outer signature. By passing a list of
    *injected* argument names, those arguments will be removed from
    the outer wrapper's signature, allowing your decorator to provide
    arguments that aren't passed in.

    Args:

        wrapper (function) : The callable to which the attributes of
            *func* are to be copied.
        func (function): The callable whose attributes are to be copied.
        injected (list): An optional list of argument names which
            should not appear in the new wrapper's signature.
        expected (list): An optional list of argument names (or (name,
            default) pairs) representing new arguments introduced by
            the wrapper (the opposite of *injected*). See
            :meth:`FunctionBuilder.add_arg()` for more details.
        build_from (function): The callable from which the new wrapper
            is built. Defaults to *func*, unless *wrapper* is partial object
            built from *func*, in which case it defaults to *wrapper*.
            Useful in some specific cases where *wrapper* and *func* have the
            same arguments but differ on which are keyword-only and positional-only.
        update_dict (bool): Whether to copy other, non-standard
            attributes of *func* over to the wrapper. Defaults to True.
        inject_to_varkw (bool): Ignore missing arguments when a
            ``**kwargs``-type catch-all is present. Defaults to True.
        hide_wrapped (bool): Remove reference to the wrapped function(s)
            in the updated function.

    In opposition to the built-in :func:`functools.update_wrapper` bolton's
    version returns a copy of the function and does not modify anything in place.
    For more in-depth wrapping of functions, see the
    :class:`FunctionBuilder` type, on which update_wrapper was built.
    """

class FunctionBuilder:
    """The FunctionBuilder type provides an interface for programmatically
    creating new functions, either based on existing functions or from
    scratch.

    Values are passed in at construction or set as attributes on the
    instance. For creating a new function based of an existing one,
    see the :meth:`~FunctionBuilder.from_func` classmethod. At any
    point, :meth:`~FunctionBuilder.get_func` can be called to get a
    newly compiled function, based on the values configured.

    >>> fb = FunctionBuilder('return_five', doc='returns the integer 5',
    ...                      body='return 5')
    >>> f = fb.get_func()
    >>> f()
    5
    >>> fb.varkw = 'kw'
    >>> f_kw = fb.get_func()
    >>> f_kw(ignored_arg='ignored_val')
    5

    Note that function signatures themselves changed quite a bit in
    Python 3, so several arguments are only applicable to
    FunctionBuilder in Python 3. Except for *name*, all arguments to
    the constructor are keyword arguments.

    Args:
        name (str): Name of the function.
        doc (str): `Docstring`_ for the function, defaults to empty.
        module (str): Name of the module from which this function was
            imported. Defaults to None.
        body (str): String version of the code representing the body
            of the function. Defaults to ``'pass'``, which will result
            in a function which does nothing and returns ``None``.
        args (list): List of argument names, defaults to empty list,
            denoting no arguments.
        varargs (str): Name of the catch-all variable for positional
            arguments. E.g., "args" if the resultant function is to have
            ``*args`` in the signature. Defaults to None.
        varkw (str): Name of the catch-all variable for keyword
            arguments. E.g., "kwargs" if the resultant function is to have
            ``**kwargs`` in the signature. Defaults to None.
        defaults (tuple): A tuple containing default argument values for
            those arguments that have defaults.
        kwonlyargs (list): Argument names which are only valid as
            keyword arguments. **Python 3 only.**
        kwonlydefaults (dict): A mapping, same as normal *defaults*,
            but only for the *kwonlyargs*. **Python 3 only.**
        annotations (dict): Mapping of type hints and so
            forth. **Python 3 only.**
        filename (str): The filename that will appear in
            tracebacks. Defaults to "boltons.funcutils.FunctionBuilder".
        indent (int): Number of spaces with which to indent the
            function *body*. Values less than 1 will result in an error.
        dict (dict): Any other attributes which should be added to the
            functions compiled with this FunctionBuilder.

    All of these arguments are also made available as attributes which
    can be mutated as necessary.

    .. _Docstring: https://en.wikipedia.org/wiki/Docstring#Python

    """

    name: Incomplete
    def __init__(self, name, **kw) -> None: ...
    def get_sig_str(self, with_annotations: bool = True):
        """Return function signature as a string.

        with_annotations is ignored on Python 2.  On Python 3 signature
        will omit annotations if it is set to False.
        """

    def get_invocation_str(self): ...
    @classmethod
    def from_func(cls, func):
        """Create a new FunctionBuilder instance based on an existing
        function. The original function will not be stored or
        modified.
        """

    def get_func(self, execdict=None, add_source: bool = True, with_dict: bool = True):
        """Compile and return a new function based on the current values of
        the FunctionBuilder.

        Args:
            execdict (dict): The dictionary representing the scope in
                which the compilation should take place. Defaults to an empty
                dict.
            add_source (bool): Whether to add the source used to a
                special ``__source__`` attribute on the resulting
                function. Defaults to True.
            with_dict (bool): Add any custom attributes, if
                applicable. Defaults to True.

        To see an example of usage, see the implementation of
        :func:`~boltons.funcutils.wraps`.
        """

    def get_defaults_dict(self):
        """Get a dictionary of function arguments with defaults and the
        respective values.
        """

    def get_arg_names(self, only_required: bool = False): ...
    defaults: Incomplete
    def add_arg(self, arg_name, default=..., kwonly: bool = False) -> None:
        """Add an argument with optional *default* (defaults to
        ``funcutils.NO_DEFAULT``). Pass *kwonly=True* to add a
        keyword-only argument
        """

    def remove_arg(self, arg_name) -> None:
        """Remove an argument from this FunctionBuilder's argument list. The
        resulting function will have one less argument per call to
        this function.

        Args:
            arg_name (str): The name of the argument to remove.

        Raises a :exc:`ValueError` if the argument is not present.

        """

class MissingArgument(ValueError): ...
class ExistingArgument(ValueError): ...

def noop(*args, **kwargs) -> None:
    """
    Simple function that should be used when no effect is desired.
    An alternative to checking for  an optional function type parameter.

    e.g.
    def decorate(func, pre_func=None, post_func=None):
        if pre_func:
            pre_func()
        func()
        if post_func:
            post_func()

    vs

    def decorate(func, pre_func=noop, post_func=noop):
        pre_func()
        func()
        post_func()
    """
