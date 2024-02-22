import re
from collections import defaultdict
from pathlib import Path

CHANGED_LINES: defaultdict[Path, dict[int, str]] = defaultdict(dict)
IGNORE_PATTERN = re.compile(r"  # type: ignore\[[a-z,\-]+\]")


def main():
    for path in Path(".").rglob("*.pyi"):
        source = path.read_text()
        if "  # type: ignore" not in source:
            continue
        lines, new_lines = source.splitlines(), []
        for i, line in enumerate(lines):
            if match := IGNORE_PATTERN.search(line):
                CHANGED_LINES[path][i] = line
                ignore = match.group()
                code, other_comment = line.split(ignore)
                if other_comment:
                    if other_comment.strip().startswith("#"):
                        new_lines.append(f"{code}{other_comment}")
                    else:
                        new_lines.append(f"{code}  # {other_comment.strip()}")
                else:
                    new_lines.append(code)
            else:
                new_lines.append(line)
        if new_lines != lines:
            path.write_text("\n".join(new_lines) + "\n")

    print(dict(CHANGED_LINES))


main()
