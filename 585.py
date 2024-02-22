import ast
import re
from collections import defaultdict
from itertools import chain
from operator import attrgetter
from pathlib import Path
from typing import NamedTuple


class DeleteableImport(NamedTuple):
    old: str
    replacement: str


STUBS_SUPPORTING_PYTHON_2 = frozenset(
    path.parent for path in Path("stubs").rglob("METADATA.toml") if "python2 = true" in path.read_text().splitlines()
)


FORBIDDEN_BUILTIN_TYPING_IMPORTS = frozenset({"List", "FrozenSet", "Set", "Dict", "Tuple"})

# AbstractSet intentionally omitted from this list -- special-cased
IMPORTED_FROM_COLLECTIONS_ABC_NOT_TYPING = frozenset(
    {
        "ByteString",
        "Collection",
        "Container",
        "ItemsView",
        "KeysView",
        "Mapping",
        "MappingView",
        "MutableMapping",
        "MutableSequence",
        "MutableSet",
        "Sequence",
        "ValuesView",
        "Iterable",
        "Iterator",
        "Generator",
        "Hashable",
        "Reversible",
        "Sized",
        "Coroutine",
        "AsyncGenerator",
        "AsyncIterable",
        "AsyncIterator",
        "Awaitable",
        "Callable",
    }
)

# The values in the mapping are what these are called in `collections`
IMPORTED_FROM_COLLECTIONS_NOT_TYPING = {
    "Counter": "Counter",
    "Deque": "deque",
    "DefaultDict": "defaultdict",
    "OrderedDict": "OrderedDict",
    "ChainMap": "ChainMap",
}


def fix_bad_syntax(path: Path) -> None:
    #    if (
    #        "@python2" in path.parts
    #        or (Path("stubs/protobuf/google/protobuf") in path.parents and str(path).endswith("_pb2.pyi"))
    #        or any(directory in path.parents for directory in STUBS_SUPPORTING_PYTHON_2)
    #        or path == Path("stdlib/typing_extensions.pyi")
    #    ):
    if path != Path("stdlib/builtins.pyi"):
        return

    #    print(f"Attempting to convert {path} to new syntax.")

    with open(path) as f:
        stub = f.read()

    lines = stub.splitlines()
    tree = ast.parse(stub)
    imports_to_delete = {}
    imports_to_add = []
    classes_from_typing = set()
    import_linenos = set()

    class BadImportFinder(ast.NodeVisitor):
        def visit_Import(self, node: ast.Import):
            import_linenos.add(node.lineno)

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            import_linenos.add(node.lineno)

            if node.module != "typing":
                return

            bad_builtins_classes_in_this_import = set()
            bad_collections_classes_in_this_import = set()
            bad_collections_abc_classes_in_this_import = set()

            for cls in node.names:
                if cls.name in FORBIDDEN_BUILTIN_TYPING_IMPORTS:
                    bad_builtins_classes_in_this_import.add(cls)
                elif cls.name in IMPORTED_FROM_COLLECTIONS_NOT_TYPING:
                    bad_collections_classes_in_this_import.add(cls)
                elif cls.name in IMPORTED_FROM_COLLECTIONS_ABC_NOT_TYPING and path not in {
                    Path("stdlib/_collections_abc.pyi"),
                    #                    Path("stdlib/builtins.pyi"),
                    Path("stdlib/types.pyi"),
                    Path("stdlib/array.pyi"),
                }:
                    bad_collections_abc_classes_in_this_import.add(cls)
                elif cls.name == "AbstractSet":
                    print(f"{path}:{node.lineno}: typing.AbstractSet")

            bad_classes_in_this_import = (
                bad_builtins_classes_in_this_import
                | bad_collections_classes_in_this_import
                | bad_collections_abc_classes_in_this_import
            )

            if not bad_classes_in_this_import:
                return

            classes_from_typing.update(cls.name for cls in bad_classes_in_this_import)
            new_import_list = [cls for cls in node.names if cls not in bad_classes_in_this_import]

            if not new_import_list:
                if path == Path("stdlib/csv.pyi"):
                    imports_to_delete[node.lineno - 1] = DeleteableImport(
                        old=ast.unparse(node), replacement="_DictReadMapping = dict"
                    )
                elif path != Path("stdlib/collections/__init__.pyi"):
                    imports_to_delete[node.lineno - 1] = DeleteableImport(old=ast.unparse(node), replacement="")
            elif node.lineno == node.end_lineno:
                imports_to_delete[node.lineno - 1] = DeleteableImport(
                    old=ast.unparse(node),
                    replacement=ast.unparse(ast.ImportFrom(module="typing", names=new_import_list, level=0)),
                )
            else:
                for cls in node.names:
                    if cls in bad_classes_in_this_import:
                        imports_to_delete[cls.lineno - 1] = DeleteableImport(
                            old=f"{cls.name}," if cls.asname is None else f"{cls.name} as {cls.asname},", replacement=""
                        )

            if bad_collections_classes_in_this_import:
                imports_to_add.append(
                    ast.unparse(
                        ast.ImportFrom(
                            module="collections",
                            names=[
                                ast.alias(name=IMPORTED_FROM_COLLECTIONS_NOT_TYPING[cls.name], asname=cls.asname)
                                for cls in sorted(bad_collections_classes_in_this_import, key=attrgetter("name"))
                            ],
                            level=0,
                        )
                    )
                )

            if bad_collections_abc_classes_in_this_import and path != Path("stdlib/collections/__init__.pyi"):
                imports_to_add.append(
                    ast.unparse(
                        ast.ImportFrom(
                            module="collections.abc",
                            names=sorted(bad_collections_abc_classes_in_this_import, key=attrgetter("name")),
                            level=0,
                        )
                    )
                )

    BadImportFinder().visit(tree)

    if not classes_from_typing:
        return

    for lineno, (old_syntax, new_syntax) in imports_to_delete.items():
        lines[lineno] = lines[lineno].replace(old_syntax, new_syntax)

    first_import_lineno = min(import_linenos) - 1

    for new_import in imports_to_add:
        lines[first_import_lineno:first_import_lineno] = [new_import]

    try:
        new_tree = ast.parse("\n".join(lines))
    except SyntaxError:
        print(path)
    else:
        lines_with_bad_syntax = defaultdict(list)

        class OldSyntaxFinder(ast.NodeVisitor):
            def visit_Subscript(self, node: ast.Subscript) -> None:
                if isinstance(node.value, ast.Name) and node.value.id in (
                    classes_from_typing & (FORBIDDEN_BUILTIN_TYPING_IMPORTS | {"Deque", "DefaultDict"})
                ):
                    lines_with_bad_syntax[node.lineno - 1].append(node.value.id)
                self.generic_visit(node)

        OldSyntaxFinder().visit(new_tree)

        for i, cls_list in lines_with_bad_syntax.items():
            for cls in cls_list:
                lines[i] = re.sub(rf"(\W){cls}\[", rf"\1{cls.lower()}[", lines[i])

    if Path("stubs\typed-ast\typed_ast") in path.parents:
        lines.remove("import typing")

    new_stub = "\n".join(lines) + "\n"

    if path == Path("stdlib/plistlib.pyi"):
        new_stub = new_stub.replace("_Dict", "dict")

    with open(path, "w") as f:
        f.write(new_stub)


def main() -> None:
    for path in chain(Path("stdlib").rglob("*.pyi"), Path("stubs").rglob("*.pyi")):
        fix_bad_syntax(path)


#    print("\n\nSTARTING ISORT...\n\n")
#    subprocess.run([sys.executable, "-m", "isort", "."])

#    print("\n\nSTARTING BLACK...\n\n")
#    subprocess.run([sys.executable, "-m", "black", "."])


if __name__ == "__main__":
    main()
