from pathlib import Path

import libcst


class ModuleFixer(libcst.CSTTransformer):
    def leave_ImportFrom(self, original_node: libcst.ImportFrom, updated_node: libcst.ImportFrom) -> libcst.ImportFrom:
        if not (isinstance(original_node.module, libcst.Name) and original_node.module.value == "_typeshed"):
            return updated_node
        if isinstance(original_node.names, libcst.ImportStar):
            return updated_node
        new_imports = [
            item
            for item in original_node.names
            if not (isinstance(item, libcst.ImportAlias) and isinstance(item.name, libcst.Name) and item.name.value == "Self")
        ]
        if len(original_node.names) == 2 and len(new_imports) == 1:
            new_imports[0] = new_imports[0].with_changes(comma=libcst.MaybeSentinel.DEFAULT)
        return updated_node.with_changes(names=new_imports)

    def leave_Parameters(self, original_node: libcst.Parameters, updated_node: libcst.Parameters) -> libcst.Parameters:
        if not original_node.params:
            return updated_node

        first_param = original_node.params[0]
        if not (isinstance(first_param, libcst.Param) and isinstance(first_param.annotation, libcst.Annotation)):
            return updated_node

        first_annotation = first_param.annotation.annotation
        if isinstance(first_annotation, libcst.Name):
            if first_annotation.value != "Self":
                return updated_node
        elif isinstance(first_annotation, libcst.Subscript):
            if not (
                isinstance(first_annotation.value, libcst.Name)
                and first_annotation.value.value == "type"
                and len(first_annotation.slice) == 1
                and isinstance(first_annotation.slice[0], libcst.SubscriptElement)
                and isinstance(first_annotation.slice[0].slice, libcst.Index)
                and isinstance(first_annotation.slice[0].slice.value, libcst.Name)
                and first_annotation.slice[0].slice.value.value == "Self"
            ):
                return updated_node
        else:
            return updated_node

        new_params = list(updated_node.params)
        new_params[0] = first_param.with_changes(annotation=None)
        return updated_node.with_changes(params=new_params)


def change_self_annotations(path: Path) -> None:
    source = path.read_text()
    if not source:
        return
    if "from _typeshed import" not in source:
        return
    if not (": Self" in source or ": type[Self]" in source):
        return
    sourcelines = source.splitlines()
    try:
        sourcelines.remove("from _typeshed import Self")
    except ValueError:
        pass
    first_non_comment_lineno = next(i for i, line in enumerate(sourcelines) if line.strip() and not line.strip().startswith("#"))
    sourcelines.insert(first_non_comment_lineno, "from typing_extensions import Self")
    cst = libcst.parse_module("\n".join(sourcelines) + "\n")
    new_source = cst.visit(ModuleFixer()).code
    path.write_text(new_source)


def main() -> None:
    for path in Path("stubs").rglob("*.pyi"):
        print(f"Fixing '{path}'...")
        change_self_annotations(path)


if __name__ == "__main__":
    main()
