from collections.abc import Sequence
import typer

# A: rock, B: paper, C: scissors
_scores = dict(A=1, B=2, C=3)

# _victory[you][me]
_victory = dict(
    A=dict(A=3, B=6, C=0),
    B=dict(A=0, B=3, C=6),
    C=dict(A=6, B=0, C=3),
)

# X: lose, Y: tie, Z: win
_move = dict(
    A=dict(X="C", Y="A", Z="B"),
    B=dict(X="A", Y="B", Z="C"),
    C=dict(X="B", Y="C", Z="A"),
)


def score(rounds: Sequence[tuple[str, str]]) -> int:
    score = 0
    for you, play in rounds:
        me = _move[you][play]
        score += _scores[me]
        score += _victory[you][me]
    return score


def main(file: typer.FileText) -> None:
    rounds = [tuple(line.strip().split()) for line in file]
    print(score(rounds))


if __name__ == "__main__":
    typer.run(main)
