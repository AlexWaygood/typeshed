import ast
import math
import re
import time
from _typeshed import Incomplete
from collections.abc import Generator
from typing import NoReturn

eval_debug: int
strTypes: tuple[type[bytes], type[str]]
isPy39: bool
isPy313: bool

class BadCode(ValueError): ...

augOps: dict[ast.operator, str]
__allowed_magic_methods__: frozenset[str]
__rl_unsafe__: frozenset[str]
__rl_unsafe_re__: re.Pattern[str]

def copy_locations(new_node, old_node) -> None: ...

class UntrustedAstTransformer(ast.NodeTransformer):
    names_seen: Incomplete
    nameIsAllowed: Incomplete
    def __init__(self, names_seen=None, nameIsAllowed=None) -> None: ...
    @property
    def tmpName(self): ...
    def error(self, node, msg) -> NoReturn: ...
    def guard_iter(self, node):
        """
        Converts:
                for x in expr
        to
                for x in __rl_getiter__(expr)

        Also used for
        * list comprehensions
        * dict comprehensions
        * set comprehensions
        * generator expresions
        """

    def is_starred(self, ob): ...
    def gen_unpack_spec(self, tpl):
        """Generate a specification for '__rl_unpack_sequence__'.

        This spec is used to protect sequence unpacking.
        The primary goal of this spec is to tell which elements in a sequence
        are sequences again. These 'child' sequences have to be protected
        again.

        For example there is a sequence like this:
                (a, (b, c), (d, (e, f))) = g

        On a higher level the spec says:
                - There is a sequence of len 3
                - The element at index 1 is a sequence again with len 2
                - The element at index 2 is a sequence again with len 2
                  - The element at index 1 in this subsequence is a sequence again
                        with len 2

        With this spec '__rl_unpack_sequence__' does something like this for
        protection (len checks are omitted):

                t = list(__rl_getiter__(g))
                t[1] = list(__rl_getiter__(t[1]))
                t[2] = list(__rl_getiter__(t[2]))
                t[2][1] = list(__rl_getiter__(t[2][1]))
                return t

        The 'real' spec for the case above is then:
                spec = {
                        'min_len': 3,
                        'childs': (
                                (1, {'min_len': 2, 'childs': ()}),
                                (2, {
                                                'min_len': 2,
                                                'childs': (
                                                        (1, {'min_len': 2, 'childs': ()})
                                                )
                                        }
                                )
                        )
                }

        So finally the assignment above is converted into:
                (a, (b, c), (d, (e, f))) = __rl_unpack_sequence__(g, spec)
        """

    def protect_unpack_sequence(self, target, value): ...
    def gen_unpack_wrapper(self, node, target, ctx: str = "store"):
        """Helper function to protect tuple unpacks.

        node: used to copy the locations for the new nodes.
        target: is the tuple which must be protected.
        ctx: Defines the context of the returned temporary node.

        It returns a tuple with two element.

        Element 1: Is a temporary name node which must be used to
                           replace the target.
                           The context (store, param) is defined
                           by the 'ctx' parameter..

        Element 2: Is a try .. finally where the body performs the
                           protected tuple unpack of the temporary variable
                           into the original target.
        """

    def gen_lambda(self, args, body): ...
    def gen_del_stmt(self, name_to_del): ...
    def transform_slice(self, slice_):
        """Transform slices into function parameters.

        ast.Slice nodes are only allowed within a ast.Subscript node.
        To use a slice as an argument of ast.Call it has to be converted.
        Conversion is done by calling the 'slice' function from builtins
        """

    def isAllowedName(self, node, name) -> None: ...
    def check_function_argument_names(self, node) -> None: ...
    def check_import_names(self, node):
        """Check the names being imported.

        This is a protection against rebinding dunder names like
        __rl_getitem__,__rl_set__ via imports.

        => 'from _a import x' is ok, because '_a' is not added to the scope.
        """

    def gen_attr_check(self, node, attr_name):
        """Check if 'attr_name' is allowed on the object in node.

        It generates (_getattr_(node, attr_name) and node).
        """

    def visit_Constant(self, node):
        """Visit the contents of a node."""

    def visit_Name(self, node): ...
    def visit_Call(self, node):
        """Checks calls with '*args' and '**kwargs'.

        Note: The following happens only if '*args' or '**kwargs' is used.

        Transfroms 'foo(<all the possible ways of args>)' into
        __rl_apply__(foo, <all the possible ways for args>)

        The thing is that '__rl_apply__' has only '*args', '**kwargs', so it gets
        Python to collapse all the myriad ways to call functions
        into one manageable from.

        From there, '__rl_apply__()' wraps args and kws in guarded accessors,
        then calls the function, returning the value.
        """

    def visit_Attribute(self, node):
        """Checks and mutates attribute access/assignment.

        'a.b' becomes '__rl_getattr__(a, "b")'
        """

    def visit_Subscript(self, node):
        """Transforms all kinds of subscripts.

        'v[a]' becomes '__rl_getitem__(foo, a)'
        'v[:b]' becomes '__rl_getitem__(foo, slice(None, b, None))'
        'v[a:]' becomes '__rl_getitem__(foo, slice(a, None, None))'
        'v[a:b]' becomes '__rl_getitem__(foo, slice(a, b, None))'
        'v[a:b:c]' becomes '__rl_getitem__(foo, slice(a, b, c))'
        'v[a,b:c] becomes '__rl_getitem__(foo, (a, slice(b, c, None)))'
        #'v[a] = c' becomes '_rl_write__(v)[a] = c'
        #'del v[a]' becomes 'del __rl_sd__(v)[a]'
        """

    def visit_Assign(self, node): ...
    def visit_AugAssign(self, node):
        """Forbid certain kinds of AugAssign

        According to the language reference (and ast.c) the following nodes
        are are possible:
        Name, Attribute, Subscript

        Note that although augmented assignment of attributes and
        subscripts is disallowed, augmented assignment of names (such
        as 'n += 1') is allowed.
        'n += 1' becomes 'n = __rl_augAssign__("+=", n, 1)'
        """
    # Bug in `reportlab`'s source code:
    def visit_While(node): ...  # type: ignore[override]
    def visit_ExceptHandler(self, node):
        """Protect tuple unpacking on exception handlers.

        try:
                .....
        except Exception as (a, b):
                ....

        becomes

        try:
                .....
        except Exception as tmp:
                try:
                        (a, b) = __rl_getiter__(tmp)
                finally:
                        del tmp
        """

    def visit_With(self, node):
        """Protect tuple unpacking on with statements."""

    def visit_FunctionDef(self, node):
        """Allow function definitions (`def`) with some restrictions."""

    def visit_Lambda(self, node):
        """Allow lambda with some restrictions."""

    def visit_ClassDef(self, node):
        """Check the name of a class definition."""

    def visit_Import(self, node): ...
    def visit_BinOp(self, node): ...
    visit_ImportFrom = visit_Import  # pyright: ignore[reportAssignmentType]
    visit_For = guard_iter
    visit_comprehension = guard_iter
    def generic_visit(self, node: ast.AST) -> None:  # type: ignore[override]
        """Reject nodes which do not have a corresponding `visit` method."""

    def not_allowed(self, node: ast.AST) -> NoReturn: ...
    def visit_children(self, node):
        """Visit the contents of a node."""

    def visit(self, node):
        """Visit a node."""
    visit_Ellipsis = not_allowed
    visit_MatMult = not_allowed
    visit_Exec = not_allowed
    visit_Nonlocal = not_allowed
    visit_AsyncFunctionDef = not_allowed
    visit_Await = not_allowed
    visit_AsyncFor = not_allowed
    visit_AsyncWith = not_allowed
    visit_Print = not_allowed
    visit_Num = visit_children
    visit_Str = visit_children
    visit_Bytes = visit_children
    visit_List = visit_children
    visit_Tuple = visit_children
    visit_Set = visit_children
    visit_Dict = visit_children
    visit_FormattedValue = visit_children
    visit_JoinedStr = visit_children
    visit_NameConstant = visit_children
    visit_Load = visit_children
    visit_Store = visit_children
    visit_Del = visit_children
    visit_Starred = visit_children
    visit_Expression = visit_children
    visit_Expr = visit_children
    visit_UnaryOp = visit_children
    visit_UAdd = visit_children
    visit_USub = visit_children
    visit_Not = visit_children
    visit_Invert = visit_children
    visit_Add = visit_children
    visit_Sub = visit_children
    visit_Mult = visit_children
    visit_Div = visit_children
    visit_FloorDiv = visit_children
    visit_Pow = visit_children
    visit_Mod = visit_children
    visit_LShift = visit_children
    visit_RShift = visit_children
    visit_BitOr = visit_children
    visit_BitXor = visit_children
    visit_BitAnd = visit_children
    visit_BoolOp = visit_children
    visit_And = visit_children
    visit_Or = visit_children
    visit_Compare = visit_children
    visit_Eq = visit_children
    visit_NotEq = visit_children
    visit_Lt = visit_children
    visit_LtE = visit_children
    visit_Gt = visit_children
    visit_GtE = visit_children
    visit_Is = visit_children
    visit_IsNot = visit_children
    visit_In = visit_children
    visit_NotIn = visit_children
    visit_keyword = visit_children
    visit_IfExp = visit_children
    visit_Index = visit_children
    visit_Slice = visit_children
    visit_ExtSlice = visit_children
    visit_ListComp = visit_children
    visit_SetComp = visit_children
    visit_GeneratorExp = visit_children
    visit_DictComp = visit_children
    visit_Raise = visit_children
    visit_Assert = visit_children
    visit_Delete = visit_children
    visit_Pass = visit_children
    visit_alias = visit_children
    visit_If = visit_children
    visit_Break = visit_children
    visit_Continue = visit_children
    visit_Try = visit_children
    visit_TryFinally = visit_children
    visit_TryExcept = visit_children
    visit_withitem = visit_children
    visit_arguments = visit_children
    visit_arg = visit_children
    visit_Return = visit_children
    visit_Yield = visit_children
    visit_YieldFrom = visit_children
    visit_Global = visit_children
    visit_Module = visit_children
    visit_Param = visit_children

def astFormat(node): ...

class __rl_SafeIter__:
    __rl_iter__: Incomplete
    __rl_owner__: Incomplete
    def __init__(self, it, owner) -> None: ...
    def __iter__(self): ...
    def __next__(self): ...
    next = __next__

__rl_safe_builtins__: Incomplete

def safer_globals(g=None): ...

math_log10 = math.log10
__rl_undef__: Incomplete

class __RL_SAFE_ENV__:
    __time_time__ = time.time
    __weakref_ref__: Incomplete
    __slicetype__: Incomplete
    timeout: Incomplete
    allowed_magic_methods: Incomplete
    __rl_gen_range__: Incomplete
    __rl_real_iter__: Incomplete
    real_bi: Incomplete
    bi_replace: Incomplete
    __rl_builtins__: Incomplete
    def __init__(self, timeout=None, allowed_magic_methods=None, allowed_magic_names=None) -> None: ...
    def __rl_type__(self, *args): ...
    def __rl_check__(self) -> None: ...
    def __rl_sd__(self, obj): ...
    def __rl_getiter__(self, it): ...
    def __rl_max__(self, arg, *args, **kwds): ...
    def __rl_min__(self, arg, *args, **kwds): ...
    def __rl_sum__(self, sequence, start: int = 0): ...
    def __rl_enumerate__(self, seq): ...
    def __rl_zip__(self, *args): ...
    def __rl_hasattr__(self, obj, name): ...
    def __rl_filter__(self, f, seq): ...
    def __rl_map__(self, f, seq): ...
    def __rl_any__(self, seq): ...
    def __rl_all__(self, seq): ...
    def __rl_sorted__(self, seq, **kwds): ...
    def __rl_reversed__(self, seq): ...
    def __rl_range__(self, start, *args): ...
    def __rl_set__(self, it): ...
    def __rl_frozenset__(self, it=()): ...
    def __rl_iter_unpack_sequence__(self, it, spec, _getiter_) -> Generator[Incomplete, None, None]:
        """Protect sequence unpacking of targets in a 'for loop'.

        The target of a for loop could be a sequence.
        For example "for a, b in it"
        => Each object from the iterator needs guarded sequence unpacking.
        """

    def __rl_unpack_sequence__(self, it, spec, _getiter_):
        """Protect nested sequence unpacking.

        Protect the unpacking of 'it' by wrapping it with '_getiter_'.
        Furthermore for each child element, defined by spec,
        __rl_unpack_sequence__ is called again.

        Have a look at transformer.py 'gen_unpack_spec' for a more detailed
        explanation.
        """

    def __rl_is_allowed_name__(self, name, crash: bool = True) -> bool:
        """Check names if they are allowed.
        If ``allow_magic_methods is True`` names in `__allowed_magic_methods__`
        are additionally allowed although their names start with `_`.
        """

    def __rl_getattr__(self, obj, a, *args): ...
    def __rl_getitem__(self, obj, a): ...
    __rl_tmax__: int
    __rl_max_len__: int
    __rl_max_pow_digits__: int
    def __rl_add__(self, a, b): ...
    def __rl_mult__(self, a, b): ...
    def __rl_pow__(self, a, b): ...
    def __rl_augAssign__(self, op, v, i): ...
    def __rl_apply__(self, func, args, kwds): ...
    def __rl_args_iter__(self, *args): ...
    def __rl_list__(self, it): ...
    def __rl_compile__(
        self, src, fname: str = "<string>", mode: str = "eval", flags: int = 0, inherit: bool = True, visit=None
    ): ...
    __rl_limit__: Incomplete
    def __rl_safe_eval__(
        self, expr, g, l, mode, timeout=None, allowed_magic_methods=None, __frame_depth__: int = 3, allowed_magic_names=None
    ): ...

class __rl_safe_eval__:
    """creates one environment and re-uses it"""

    mode: str
    env: Incomplete
    def __init__(self) -> None: ...
    def __call__(self, expr, g=None, l=None, timeout=None, allowed_magic_methods=None, allowed_magic_names=None): ...

class __rl_safe_exec__(__rl_safe_eval__):
    mode: str

def rl_extended_literal_eval(expr, safe_callables=None, safe_names=None): ...

rl_safe_exec: __rl_safe_exec__
rl_safe_eval: __rl_safe_eval__

def __fix_set__(value, default=...): ...
def rl_less_safe_eval(expr, NS):
    """eval with our so called safe globals"""
