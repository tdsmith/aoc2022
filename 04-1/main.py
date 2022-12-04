import attr
import typer
from typing_extensions import Self


@attr.define(frozen=True)
class Range:
    start: int
    stop: int

    @classmethod
    def parse(cls, spec: str) -> Self:
        start, stop = [int(i) for i in spec.split("-")]
        return cls(start, stop)


def _sort_key(range: Range) -> tuple[int, ...]:
    return (range.start, -range.stop)


def contains_completely(r1: Range, r2: Range) -> bool:
    left, right = sorted([r1, r2], key=_sort_key)
    return right.stop <= left.stop


def test(a1: int, a2: int, b1: int, b2: int, truthy: bool) -> None:
    assert contains_completely(Range(a1, a2), Range(b1, b2)) == truthy


test(1, 1, 1, 1, True)
test(1, 2, 1, 2, True)
test(1, 2, 0, 4, True)
test(0, 4, 1, 2, True)
test(0, 4, 0, 2, True)
test(0, 2, 0, 4, True)


def count_contains_completely(ranges: list[tuple[Range, Range]]) -> int:
    return len([1 for r1, r2 in ranges if contains_completely(r1, r2)])


def main(file: typer.FileText) -> None:
    ranges = [
        tuple(Range.parse(spec) for spec in line.strip().split(",")) for line in file
    ]
    print(count_contains_completely(ranges))


if __name__ == "__main__":
    typer.run(main)
