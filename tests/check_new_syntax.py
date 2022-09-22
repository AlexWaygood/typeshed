#!/usr/bin/env python3

from __future__ import annotations

import ast
import sys
from itertools import chain
from pathlib import Path

from config import get_typeshed_config
from utils import minor_version_from_version_string


def check_new_syntax(tree: ast.AST, path: Path, stub: str, minimum_minor_version: int) -> list[str]:
    errors = []
    sourcelines = stub.splitlines()

    class AnnotationUnionFinder(ast.NodeVisitor):
        def visit_Subscript(self, node: ast.Subscript) -> None:
            if isinstance(node.value, ast.Name):
                if node.value.id == "Union" and isinstance(node.slice, ast.Tuple):
                    new_syntax = " | ".join(ast.unparse(x) for x in node.slice.elts)
                    errors.append(f"{path}:{node.lineno}: Use PEP 604 syntax for Union, e.g. `{new_syntax}`")
                if node.value.id == "Optional":
                    new_syntax = f"{ast.unparse(node.slice)} | None"
                    errors.append(f"{path}:{node.lineno}: Use PEP 604 syntax for Optional, e.g. `{new_syntax}`")

            self.generic_visit(node)

    class NonAnnotationUnionFinder(ast.NodeVisitor):
        def visit_Subscript(self, node: ast.Subscript) -> None:
            if isinstance(node.value, ast.Name):
                nodelines = sourcelines[(node.lineno - 1) : node.end_lineno]
                for line in nodelines:
                    # A hack to workaround various PEP 604 bugs in mypy
                    if any(x in line for x in {"tuple[", "Callable[", "type["}):
                        return None
                if node.value.id == "Union" and isinstance(node.slice, ast.Tuple):
                    new_syntax = " | ".join(ast.unparse(x) for x in node.slice.elts)
                    errors.append(f"{path}:{node.lineno}: Use PEP 604 syntax for Union, e.g. `{new_syntax}`")
                elif node.value.id == "Optional":
                    new_syntax = f"{ast.unparse(node.slice)} | None"
                    errors.append(f"{path}:{node.lineno}: Use PEP 604 syntax for Optional, e.g. `{new_syntax}`")

            self.generic_visit(node)

    class OldSyntaxFinder(ast.NodeVisitor):
        def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
            AnnotationUnionFinder().visit(node.annotation)
            if node.value is not None:
                NonAnnotationUnionFinder().visit(node.value)
            self.generic_visit(node)

        def visit_arg(self, node: ast.arg) -> None:
            if node.annotation is not None:
                AnnotationUnionFinder().visit(node.annotation)
            self.generic_visit(node)

        def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            if node.returns is not None:
                AnnotationUnionFinder().visit(node.returns)
            self.generic_visit(node)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self._visit_function(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self._visit_function(node)

        def visit_Assign(self, node: ast.Assign) -> None:
            NonAnnotationUnionFinder().visit(node.value)
            self.generic_visit(node)

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            for base in node.bases:
                NonAnnotationUnionFinder().visit(base)
            self.generic_visit(node)

    class IfOrderChecker(ast.NodeVisitor):
        def visit_If(self, node: ast.If) -> None:
            if (
                isinstance(node.test, ast.Compare)
                and ast.unparse(node.test).startswith("sys.version_info < ")
                and node.orelse
                and not (len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If))  # elif statement (#6728)
            ):
                new_syntax = "if " + ast.unparse(node.test).replace("<", ">=", 1)
                errors.append(
                    f"{path}:{node.lineno}: When using if/else with sys.version_info, "
                    f"put the code for new Python versions first, e.g. `{new_syntax}`"
                )
            self.generic_visit(node)

    class MinVersionChecker(ast.NodeVisitor):
        def visit_If(self, node: ast.If) -> None:
            self.generic_visit(node)
            if (
                isinstance(node.test, ast.Compare)
                and isinstance(node.test.left, ast.Attribute)
                and isinstance(node.test.left.value, ast.Name)
                and node.test.left.value.id == "sys"
                and node.test.left.attr == "version_info"
                and len(node.test.ops) == 1
                and len(node.test.comparators) == 1
                and isinstance(node.test.comparators[0], ast.Tuple)
                and len(node.test.comparators[0].elts) == 2
            ):
                op = node.test.ops[0]
                major_ver_elt, minor_ver_elt = node.test.comparators[0].elts

                if isinstance(major_ver_elt, ast.Constant) and isinstance(major_ver_elt.value, int):
                    major_ver = major_ver_elt.value
                else:
                    errors.append(f"{path}:{node.lineno}: Invalid `sys.version_info` check")
                    return

                if isinstance(minor_ver_elt, ast.Constant) and isinstance(minor_ver_elt.value, int):
                    minor_ver = minor_ver_elt.value
                else:
                    errors.append(f"{path}:{node.lineno}: Invalid `sys.version_info` check")
                    return

                if major_ver != 3:
                    errors.append(
                        f"{path}:{node.lineno}: Redundant `sys.version_info` check (typeshed only supports Python 3)"
                    )
                    return

                if isinstance(op, (ast.GtE, ast.Lt)):
                    if minor_ver <= minimum_minor_version:
                        errors.append(
                            f"{path}:{node.lineno}: Redundant `sys.version_info` check "
                            f"(3.{minimum_minor_version} is the lowest Python version supported by typeshed)"
                        )
                else:
                    errors.append(
                        f"{path}:{node.lineno}: Invalid `sys.version_info` check "
                        f'(must use either "<" or ">=", not {ast.unparse(op)}'
                    )

    OldSyntaxFinder().visit(tree)
    IfOrderChecker().visit(tree)
    MinVersionChecker().visit(tree)
    return errors


def main() -> None:
    errors = []
    config = get_typeshed_config()
    minimum_minor_version = minor_version_from_version_string(config.min_supported_version)
    for path in chain(Path("stdlib").rglob("*.pyi"), Path("stubs").rglob("*.pyi")):
        with open(path) as f:
            stub = f.read()
            tree = ast.parse(stub)
        errors.extend(check_new_syntax(tree, path, stub, minimum_minor_version))

    if errors:
        print("\n".join(errors))
        sys.exit(1)


if __name__ == "__main__":
    main()
