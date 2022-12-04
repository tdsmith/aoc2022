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


def overlaps(r1: Range, r2: Range) -> bool:
    # left is the longest segment with the leftmost start
    left, right = sorted([r1, r2], key=_sort_key)
    return left.stop >= right.start


def count_overlaps(ranges: list[tuple[Range, Range]]) -> int:
    return len([1 for r1, r2 in ranges if overlaps(r1, r2)])


def main(file: typer.FileText) -> None:
    ranges = [
        tuple(Range.parse(spec) for spec in line.strip().split(",")) for line in file
    ]
    print(count_overlaps(ranges))


if __name__ == "__main__":
    typer.run(main)
