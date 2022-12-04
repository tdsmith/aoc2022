import typer


def shared_item(rucksack: str) -> str:
    assert len(rucksack) % 2 == 0
    n = len(rucksack)
    (item,) = set(rucksack[: n // 2]).intersection(rucksack[n // 2 :])
    return item


def priority(item: str) -> int:
    assert len(item) == 1
    if item < "a":
        priority = ord(item) - ord("A") + 27
    else:
        priority = ord(item) - ord("a") + 1
    return priority


def priority_sums(rucksacks: list[str]) -> int:
    score = 0
    for sack in rucksacks:
        score += priority(shared_item(sack))
    return score


def main(file: typer.FileText) -> None:
    rucksacks = [line.strip() for line in file]
    print(priority_sums(rucksacks))


if __name__ == "__main__":
    typer.run(main)
