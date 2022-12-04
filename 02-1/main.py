from collections.abc import Sequence
import typer

_scores = dict(A=1, B=2, C=3, X=1, Y=2, Z=3)

# _victory[you][me]
_victory = dict(
    A=dict(X=3, Y=6, Z=0),
    B=dict(X=0, Y=3, Z=6),
    C=dict(X=6, Y=0, Z=3),
)


def score(rounds: Sequence[tuple[str, str]]) -> int:
    score = 0
    for you, me in rounds:
        score += _scores[me]
        score += _victory[you][me]
    return score


def main(file: typer.FileText) -> None:
    rounds = [tuple(line.strip().split()) for line in file]
    print(score(rounds))


if __name__ == "__main__":
    typer.run(main)
