from functools import reduce
from itertools import islice
from typing import Iterable

import typer


def shared_item(rucksacks: Iterable[str]) -> str:
    (item,) = reduce(set.intersection, (set(sack) for sack in rucksacks))
    return item


def priority(item: str) -> int:
    assert len(item) == 1
    if item < "a":
        priority = ord(item) - ord("A") + 27
    else:
        priority = ord(item) - ord("a") + 1
    return priority


def shared_item_priority_sums(rucksacks: list[str]) -> int:
    i = iter(rucksacks)
    score = 0
    while squad := list(islice(i, 3)):
        score += priority(shared_item(squad))
    return score


def main(file: typer.FileText) -> None:
    rucksacks = [line.strip() for line in file]
    print(shared_item_priority_sums(rucksacks))


if __name__ == "__main__":
    typer.run(main)
