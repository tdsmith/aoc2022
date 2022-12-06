import typer


def find_first_marker(s: str, k: int) -> int | None:
    for i in range(k, len(s)):
        if len(set(s[i - k : i])) == k:
            return i


def main(file: typer.FileText) -> None:
    for line in file:
        line = line.strip()
        print(find_first_marker(line, 4), end=", ")
        print(find_first_marker(line, 14))


if __name__ == "__main__":
    typer.run(main)
