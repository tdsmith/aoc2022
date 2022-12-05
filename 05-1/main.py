import copy
import re

import attr
import typer


@attr.define(frozen=True)
class Command:
    n: int
    origin: int
    dest: int


StackT = dict[int, list[str]]


def eval_commands(stacks: StackT, commands: list[Command]) -> StackT:
    stacks = copy.deepcopy(stacks)
    for command in commands:
        for _ in range(command.n):
            stacks[command.dest].append(stacks[command.origin].pop())
    return stacks


def top_after_eval(stacks: StackT, commands: list[Command]) -> str:
    new_stacks = eval_commands(stacks, commands)
    tops = []
    for stack in sorted(new_stacks):
        tops.append(new_stacks[stack][-1])
    return "".join(tops)


def main(file: typer.FileText) -> None:
    stacks = {}
    for line in file:
        matches = list(re.finditer(r"\[(\w)\]", line))
        if not matches:
            break
        for match in matches:
            assert match.start() % 4 == 0
            stack = match.start() // 4 + 1
            stacks.setdefault(stack, []).append(match[1])
    for stack in stacks:
        stacks[stack] = list(reversed(stacks[stack]))

    commands = []
    for line in file:
        match = re.match(r"move (\d+) from (\d+) to (\d+)$", line)
        if not match:
            continue
        commands.append(Command(*[int(i) for i in match.groups()]))

    print(top_after_eval(stacks, commands))


if __name__ == "__main__":
    typer.run(main)
