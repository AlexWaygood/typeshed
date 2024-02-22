import ast
import inspect
import sys
import textwrap
import traceback
import warnings
from collections.abc import Collection
from pathlib import Path


def is_name(obj: ast.AST, name: str | Collection[str]) -> bool:
    if not isinstance(obj, ast.Name):
        return False
    if isinstance(name, str):
        return obj.id == name
    return obj.id in name


warnings.filterwarnings("ignore", category=DeprecationWarning)


def check_syntax(tree: ast.AST, path: Path) -> list[str]:
    errors = []
    skipped_modules = set()

    class RuntimeReturnStatementFinder(ast.NodeVisitor):
        return_statement_values: list[ast.expr | None]
        await_statements: list[ast.Await]
        yield_statements: list[ast.Yield]
        yield_froms: list[ast.YieldFrom]
        is_classmethod: bool
        has_raiseNotImplementedError: bool

        def __init__(self, *, is_classmethod: bool) -> None:
            self.return_statement_values = []
            self.await_statements = []
            self.yield_statements = []
            self.yield_froms = []
            self.is_classmethod = is_classmethod
            self.has_raiseNotImplementedError = False

        def visit_Return(self, node: ast.Return) -> None:
            self.return_statement_values.append(node.value)
            self.generic_visit(node)

        def visit_Await(self, node: ast.Await) -> None:
            self.await_statements.append(node)
            self.generic_visit(node)

        def visit_Yield(self, node: ast.Yield) -> None:
            self.yield_statements.append(node)
            self.generic_visit(node)

        def visit_YieldFrom(self, node: ast.YieldFrom) -> None:
            self.yield_froms.append(node)
            self.generic_visit(node)

        def visit_Raise(self, node: ast.Raise) -> None:
            exc = node.exc
            if isinstance(exc, ast.Name):
                exc_id = exc.id
            elif isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name):
                exc_id = exc.func.id
            else:
                return
            if exc_id == "NotImplementedError":
                self.has_raiseNotImplementedError = True
            self.generic_visit(node)

    class FunctionFinder(ast.NodeVisitor):
        def __init__(self) -> None:
            self.current_class_name = ""
            self.protocol_name = ""

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            old_name = self.current_class_name
            self.current_class_name = node.name
            if not self.protocol_imported or not any(
                is_name(base, self.protocol_name) or (isinstance(base, ast.Subscript) and is_name(base.value, self.protocol_name))
                for base in node.bases
            ):
                self.generic_visit(node)
            self.current_class_name = old_name

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            module_name, imported_objects = node.module, node.names

            if module_name != "typing":
                return

            for imported_obj in node.names:
                if imported_obj.name != "Protocol":
                    continue
                self.protocol_name = "Protocol" if imported_obj.asname is None else imported_obj.asname
                break

        @property
        def in_class(self) -> bool:
            return bool(self.current_class_name)

        @property
        def protocol_imported(self) -> bool:
            return bool(self.protocol_name)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.generic_visit(node)

            if not self.in_class:
                return
            decorators = node.decorator_list
            if any(is_name(deco, ("staticmethod", "abstractmethod")) for deco in decorators):
                return
            is_classmethod = any(is_name(deco, "classmethod") for deco in decorators)
            return_annotation = node.returns

            runtime_module_as_string = ".".join(path.parts[1:-1])

            if path.parts[-1] != "__init__.pyi":
                if runtime_module_as_string:
                    runtime_module_as_string += "."
                runtime_module_as_string += path.parts[-1].split(".")[0]

            if runtime_module_as_string == "antigravity":  # It was amusing the first time it happened, but no
                return

            try:
                runtime_module = __import__(runtime_module_as_string)
            except ModuleNotFoundError:
                if runtime_module_as_string not in skipped_modules:
                    skipped_modules.add(runtime_module_as_string)
                    print(f"Skipping {runtime_module_as_string}: Does not appear to exist on this system")
                return
            except ImportError:
                if runtime_module_as_string not in skipped_modules:
                    skipped_modules.add(runtime_module_as_string)
                    print(f"Skipping {runtime_module_as_string}: {traceback.format_exc().splitlines()[-1]}")
                return

            if self.current_class_name:
                try:
                    runtime_class = getattr(runtime_module, self.current_class_name)
                except AttributeError:
                    return
            else:
                runtime_class = runtime_module
            try:
                runtime_function = getattr(runtime_class, node.name)
            except AttributeError:
                return

            full_func_name = f"{self.current_class_name}.{node.name}"

            try:
                source = inspect.getsource(runtime_function)
            except TypeError:
                return
            except OSError:
                print(f"Skipping {runtime_module_as_string}.{full_func_name}: OSError: Could not get the source")
                return

            cleaned_runtime_source_code = textwrap.dedent(source)

            try:
                runtime_ast = ast.parse(cleaned_runtime_source_code)
            except IndentationError:
                print(f"Skipping {runtime_module_as_string}.{full_func_name}: IndentationError")
                return

            return_finder = RuntimeReturnStatementFinder(is_classmethod=is_classmethod)
            return_finder.visit(runtime_ast)
            yields, return_values, awaits, yield_froms, has_raiseNotImplementedError = (
                return_finder.yield_statements,
                return_finder.return_statement_values,
                return_finder.await_statements,
                return_finder.yield_froms,
                return_finder.has_raiseNotImplementedError,
            )

            if (
                isinstance(runtime_class, type)
                and (
                    (isinstance(runtime_class.__doc__, str) and "abstract" in runtime_class.__doc__.lower())
                    or (isinstance(runtime_function.__doc__, str) and "abstract" in runtime_function.__doc__.lower())
                )
                and has_raiseNotImplementedError
            ):
                errors.append(
                    f"{path}:{node.lineno}: {full_func_name} is abstract at runtime, but isn't decorated with @abstractmethod"
                )

            if return_annotation is None or is_name(return_annotation, ("NoReturn", "Any")):
                return

            if yields or awaits or yield_froms:
                return

            if not return_values or all(
                (isinstance(return_value, ast.Constant) and return_value.value is None) for return_value in return_values
            ):
                if not (isinstance(return_annotation, ast.Constant) and return_annotation.value is None):
                    errors.append(
                        f'{path}:{node.lineno}: {full_func_name} never returns, but typeshed stub does not return "None"'
                    )
                return

            if isinstance(return_annotation, ast.Name) and return_annotation.id == "Self":
                return

            if is_classmethod:
                if all(
                    (
                        isinstance(return_value, ast.Call)
                        and isinstance(return_value.func, ast.Name)
                        and return_value.func.id == "cls"
                    )
                    for return_value in return_values
                ):
                    errors.append(
                        f'{path}:{node.lineno}: {full_func_name} only ever returns "self" but typeshed stub does not return "Self"'
                    )
                return

            if all(isinstance(return_value, ast.Name) and return_value.id == "self" for return_value in return_values):
                errors.append(
                    f'{path}:{node.lineno}: {full_func_name} only ever returns "self" but typeshed stub does not return "Self"'
                )
            return

        visit_AsyncFunctionDef = visit_FunctionDef  # type: ignore

    FunctionFinder().visit(tree)
    return errors


ALLOWLIST = frozenset(
    {
        Path("stdlib/typing.pyi"),
        Path("stdlib/typing_extensions.pyi"),
        Path("stdlib/smtpd.pyi"),
        Path("stdlib/numbers.pyi"),
        Path("stdlib/bdb.pyi"),
        Path("stdlib/ssl.pyi"),
        Path("stdlib/pdb.pyi"),
        Path("stdlib/codecs.pyi"),
    }
)


def main() -> None:
    errors = []
    for path in Path("stdlib").rglob("*.pyi"):
        if "@python2" in path.parts or "asyncio" in path.parts or path in ALLOWLIST:
            continue
        with open(path) as f:
            tree = ast.parse(f.read())
        errors.extend(check_syntax(tree, path))

    if errors:
        print("\n\nFound errors!\n\n")
        print("\n".join(errors))
        sys.exit(1)


if __name__ == "__main__":
    main()
