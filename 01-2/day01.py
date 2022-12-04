import heapq
import timeit

import typer

def part1(input: list[int | None], display: bool = False) -> None:
    elfmax = 0
    elf = 0
    for snack in input:
        if snack:
            elf += snack
            continue
        elfmax = max(elf, elfmax)
        elf = 0
    if display:
        print(elfmax)

def part2(input: list[int | None], display: bool = False) -> None:
    elfmax = [0, 0, 0]
    elf = 0
    for snack in input:
        if snack:
            elf += snack
            continue
        if elf > elfmax[0]:
            elfmax = sorted([elf, *elfmax])[1:]
        elf = 0
    if display:
        print(elfmax)
        print(sum(elfmax))

def part2_heapq(input: list[int | None], display: bool = False) -> None:
    heap = [0, 0, 0]
    elf = 0
    for snack in input:
        if snack:
            elf += snack
            continue
        heapq.heappushpop(heap, elf)
        elf = 0
    if display:
        print(heap)
        print(sum(heap))

def part2_heapq2(input: list[int | None], display: bool = False) -> None:
    heap = [0, 0, 0]
    elf = 0
    for snack in input:
        if snack:
            elf += snack
            continue
        if elf > heap[0]:
            heapq.heapreplace(heap, elf)
        elf = 0
    if display:
        print(heap)
        print(sum(heap))

input: list[int | None] = []

def main(file: typer.FileText) -> None:
    global input
    for line in file:
        line = line.strip()
        input.append(int(line) if line else None)
    input.append(None)
    for f in (part1, part2, part2_heapq, part2_heapq2):
        s = timeit.repeat(f"{f.__name__}(input)", globals=globals(), number=5000)
        print(f"{f.__name__}: {min(s)} sec")
        f(input, True)
        print()


if __name__ == "__main__":
    typer.run(main)
