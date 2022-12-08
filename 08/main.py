import numpy as np
import typer


def visible(arr: np.ndarray) -> int:
    rows, cols = arr.shape
    visible = 0
    visible_arr = np.full_like(arr, " ")
    for r in range(rows):
        for c in range(cols):
            up = arr[0:r, c]
            left = arr[r, 0:c]
            right = arr[r, c + 1 :]
            down = arr[r + 1 :, c]
            for sightline in (up, left, right, down):
                if sightline.size == 0:
                    visible += 1
                    visible_arr[r, c] = "*"
                    break
                if all(step < arr[r, c] for step in sightline):
                    visible += 1
                    visible_arr[r, c] = "*"
                    break
    print(visible_arr)
    return visible


def treed(arr: np.ndarray) -> int:
    rows, cols = arr.shape
    max_score = 0
    scores = np.zeros_like(arr)
    for r in range(rows):
        for c in range(cols):
            up = arr[0:r, c]
            left = arr[r, 0:c]
            right = arr[r, c + 1 :]
            down = arr[r + 1 :, c]
            score = 1
            for sightline in (reversed(up), reversed(left), right, down):
                dist = 0
                for i in sightline:
                    dist += 1
                    if i >= arr[r, c]:
                        break
                score *= dist
            scores[r, c] = score
            max_score = max(score, max_score)
    print(scores)
    return max_score


def main(file: typer.FileText):
    grid = []
    for line in file:
        grid.append(list(line.strip()))
    npgrid = np.asarray(grid)
    print(visible(npgrid))
    print(treed(npgrid))


if __name__ == "__main__":
    typer.run(main)
