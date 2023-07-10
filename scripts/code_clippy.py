import json
import re
import sys
import subprocess
from itertools import chain
from pathlib import Path
from typing import TypedDict

def get_new_pyi_linenos(reference_commit: str) -> dict[Path, set[int]]:
    raw_diff = subprocess.run(["git", "diff", "-U0", reference_commit], capture_output=True, text=True, check=True).stdout
    interesting_lines = "\n".join(line for line in raw_diff.splitlines() if not line.startswith(("-", "+", "index ")))
    matches = chain(
        re.finditer(r"diff --git a/\S+ b/(\S+)\n(.*?)(?=diff)", interesting_lines, flags=re.DOTALL),
        re.finditer(r"diff --git a/\S+ b/(\S+)\n(.*)$", interesting_lines)
    )
    per_file_diff = {filename: match[2] for match in matches if (filename := match[1]).endswith(".pyi")}
    new_lines: dict[str, set[int]] = {}
    for filename, diff in per_file_diff.items():
        line_ranges = (match[1] for match in re.finditer(r"@@ -\S+ \+(\d+,?\d*) @@", diff))
        changed_lines = set[int]()
        for line_range in line_ranges:
            if "," in line_range:
                start, steps = map(int, line_range.split(","))
                changed_lines.update(range(start, start + steps))
            else:
                changed_lines.add(int(line_range))
        if changed_lines:
            new_lines[Path(filename)] = changed_lines
    return new_lines


class Flake8Error(TypedDict):
    code: str
    filename: str
    line_number: int
    column_number: int
    text: str
    physical_line: str


def get_flake8_errors() -> dict[Path, list[Flake8Error]]:
    proc = subprocess.run(
        [sys.executable, "-m", "flake8", "stdlib", "stubs", "--select", "Y090", "--exit-zero", "--format", "json"],
        capture_output=True,
        text=True,
        check=True
    )
    return {Path(filename): errors for filename, errors in json.loads(proc.stdout).items() if errors}


def get_errors_on_changed_lines(new_pyi_lines: dict[str, set[int]], flake8_errors: dict[str, Flake8Error]) -> list[str]:
    errors: list[str] = []
    for path, per_file_errors in flake8_errors.items():
        changed_lines_in_this_file = new_pyi_lines.get(path, set())
        if changed_lines_in_this_file:
            errors.extend(
                f"{path.as_posix()}:{error['line_number']}:{error['column_number']}: {error['code']} {error['text']}"
                for error in per_file_errors
                if error["line_number"] in changed_lines_in_this_file
            )
    return errors


def main(reference_commit: str) -> None:
    new_pyi_linenos = get_new_pyi_linenos(reference_commit)
    flake8_errors = get_flake8_errors()
    for error in get_errors_on_changed_lines(new_pyi_linenos, flake8_errors):
        print(error)


if __name__ == "__main__":
    main(sys.argv[1])
