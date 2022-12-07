import re
from typing import Any, Sequence

import typer


def _size_directory(
    tree: dict, prefix: tuple[str, ...], sized: dict[tuple[str, ...], int]
) -> int:
    size = 0
    for k, v in tree.items():
        if isinstance(v, dict):
            stem = (*prefix, k)
            sized[stem] = _size_directory(v, stem, sized)
            size += sized[stem]
        else:
            size += v
    return size


def directory_sizes(tree: dict) -> dict[tuple[str, ...], int]:
    sized: dict[tuple[str, ...], int] = {}
    sized[()] = _size_directory(tree, (), sized)
    return sized


def set_in(d: dict, path: Sequence[str], key: str, value: Any) -> None:
    for part in path:
        d = d.setdefault(part, {})
    d[key] = value


def main(file: typer.FileText):
    tree = {}
    pwd = []
    for line in file:
        if match := re.match(r"^\$ cd (.*)$", line):
            if match[1] == "/":
                pwd = []
            elif match[1] == "..":
                pwd = pwd[:-1]
            else:
                pwd = [*pwd, match[1]]
        elif match := re.match(r"^(\d+) (.*)$", line):
            set_in(tree, pwd, match[2], int(match[1]))

    sized = directory_sizes(tree)
    print(sum(v for v in sized.values() if v <= 100000))

    ## part 2
    available_space = 70000000 - sized[()]
    space_to_free = 30000000 - available_space
    sorted_sizes = sorted(sized.values())
    for size in sorted_sizes:
        if size > space_to_free:
            print(size)
            break


if __name__ == "__main__":
    typer.run(main)
