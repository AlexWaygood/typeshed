import ast
import re
import subprocess
import sys
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
from typing import Iterator

FAILURES = []


@dataclass
class NestingCounter:
    """Class to help the PyiVisitor keep track of internal state"""

    nesting: int = 0

    @contextmanager
    def enabled(self) -> Iterator[None]:
        self.nesting += 1
        try:
            yield
        finally:
            self.nesting -= 1

    @property
    def active(self) -> bool:
        """Determine whether the level of nesting is currently non-zero"""
        return bool(self.nesting)


class AnnotationFinder(ast.NodeVisitor):
    def __init__(self) -> None:
        self.all_names = set[str]()

    def visit_Attribute(self, node: ast.Attribute) -> None:
        return

    def visit_Name(self, node: ast.Name) -> None:
        self.all_names.add(node.id)
        self.generic_visit(node)


def fix_bad_syntax(path: Path) -> None:
    with open(path) as f:
        stub = f.read()

    lines = stub.splitlines()
    tree = ast.parse(stub)
    typealias_import_needed = False

    class StubVisitor(ast.NodeVisitor):
        def __init__(self) -> None:
            # Mapping of all assignments in the file that could be type aliases
            # (This excludes assignments to function calls and ellipses, etc.)
            self.maybe_typealias_assignments: defaultdict[str, list[ast.Assign]] = defaultdict(list)
            # Set of all names and attributes that are used as annotations in the file
            self.all_names_in_annotations: set[str] = set()
            self.in_class = NestingCounter()

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            with self.in_class.enabled():
                self.generic_visit(node)

        def visit_annotation(self, annotation: ast.expr) -> None:
            annotation_finder = AnnotationFinder()
            annotation_finder.visit(annotation)
            self.all_names_in_annotations |= annotation_finder.all_names

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            returns = node.returns
            if node.returns is not None:
                self.visit_annotation(node.returns)
            self.generic_visit(node)

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_arg(self, node: ast.arg) -> None:
            annotation = node.annotation
            if annotation is not None:
                self.visit_annotation(annotation)
            self.generic_visit(node)

        def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
            self.visit_annotation(node)
            self.generic_visit(node)

        def visit_Assign(self, node: ast.Assign) -> None:
            nonlocal typealias_import_needed
            self.generic_visit(node)
            target = node.targets[0]
            assert isinstance(target, ast.Name)
            target_name = target.id
            if not target_name.startswith("_"):
                return
            if (self.in_class.active and target_name == "__match_args__") or (
                target_name == "__all__" and not self.in_class.active
            ):
                return
            assignment = node.value
            if isinstance(assignment, (ast.Ellipsis, ast.Call, ast.Num, ast.Str, ast.Bytes)):
                return

            if isinstance(assignment, ast.Name):
                self.maybe_typealias_assignments[target_name].append(node)
            elif isinstance(assignment, ast.Attribute):
                if isinstance(assignment.value, ast.Name):
                    self.maybe_typealias_assignments[target_name].append(node)
            elif "# noqa: Y026" not in lines[node.lineno - 1]:
                typealias_import_needed = True
                lines[node.lineno - 1] = re.sub(f"{target_name} = ", f"{target_name}: TypeAlias = ", lines[node.lineno - 1])

        def visit(self, tree: ast.AST) -> None:
            nonlocal typealias_import_needed
            super().visit(tree)
            for annotation in self.all_names_in_annotations:
                for node in self.maybe_typealias_assignments[annotation]:
                    if "# noqa: Y026" not in lines[node.lineno - 1]:
                        typealias_import_needed = True
                        lines[node.lineno - 1] = re.sub(f"{annotation} = ", f"{annotation}: TypeAlias = ", lines[node.lineno - 1])

    StubVisitor().visit(tree)

    if not typealias_import_needed:
        return

    tree = ast.parse("\n".join(lines))
    typealias_imported = False

    class TypeAliasImportFinder(ast.NodeVisitor):
        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            nonlocal typealias_imported

            if node.module != "typing_extensions":
                return

            if any(cls.name == "TypeAlias" for cls in node.names):
                typealias_imported = True
            return

    TypeAliasImportFinder().visit(tree)

    if not typealias_imported:
        lines = ["from typing_extensions import TypeAlias"] + lines

    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def main() -> None:
    print("STARTING RUN: Will attempt to fix new syntax in the stubs directory...\n\n")
    for path in chain(Path("stdlib").rglob("*.pyi"), Path("stubs").rglob("*.pyi")):
        if "@python2" in path.parts:
            continue
        print(f"Attempting to convert {path} to new syntax.")
        fix_bad_syntax(path)

    print("\n\nSTARTING ISORT...\n\n")
    subprocess.run([sys.executable, "-m", "isort", "."])

    print("\n\nSTARTING BLACK...\n\n")
    subprocess.run([sys.executable, "-m", "black", "."])

    if FAILURES:
        print("\n\nFAILED to convert the following files to new syntax:\n")
        for path in FAILURES:
            print(f"- {path}")
    else:
        print("\n\nThere were ZERO failures in converting to new syntax. HOORAY!!\n\n")

    print('\n\nRunning "check_new_syntax.py"...\n\n')
    subprocess.run([sys.executable, "tests/check_new_syntax.py"])


if __name__ == "__main__":
    main()
