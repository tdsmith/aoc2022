import typer


def find_first_marker(s: str) -> int:
    for i in range(4, len(s)):
        if len(set(s[i - 4 : i])) == 4:
            return i
    raise ValueError()


def main(file: typer.FileText) -> None:
    for line in file:
        line = line.strip()
        print(find_first_marker(line))


if __name__ == "__main__":
    typer.run(main)
