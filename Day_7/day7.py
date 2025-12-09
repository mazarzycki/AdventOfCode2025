from pathlib import Path
from functools import lru_cache


def read_grid(filename: str = "day7_data.txt") -> list[str]:
    data_path = Path(__file__).parent / filename
    if not data_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {data_path!s}.\n"
            "Make sure you're running the script from the correct folder."
        )

    with data_path.open() as f:
        grid = [line.rstrip("\n") for line in f]

    width = len(grid[0])
    if any(len(row) != width for row in grid):
        raise ValueError("Grid rows have inconsistent length.")
    return grid


def find_start(grid: list[str]) -> tuple[int, int]:
    """Find the coordinates of 'S' in the grid."""
    for r, line in enumerate(grid):
        c = line.find("S")
        if c != -1:
            return r, c
    raise ValueError("No starting position 'S' found in grid.")


def count_splits(grid: list[str]) -> int:
    height = len(grid)
    width = len(grid[0])

    start_row, start_col = find_start(grid)

    # Start the beam at S; treat S like empty space.
    beams = {(start_row, start_col)}
    split_count = 0

    # Each step, all beams move exactly one row down (or disappear).
    while beams:
        new_beams = set()

        for r, c in beams:
            # If outside grid, this beam is gone.
            if r < 0 or r >= height or c < 0 or c >= width:
                continue

            cell = grid[r][c]

            if cell in (".", "S"):
                # Just moves straight down.
                nr = r + 1
                if nr < height:
                    new_beams.add((nr, c))

            elif cell == "^":
                # Beam stops here and splits into two beams
                # that start one row below, diagonally left and right.
                split_count += 1
                nr = r + 1
                if nr < height:
                    if c - 1 >= 0:
                        new_beams.add((nr, c - 1))
                    if c + 1 < width:
                        new_beams.add((nr, c + 1))

            else:
                # Unexpected char: treat as empty (safe fallback).
                nr = r + 1
                if nr < height:
                    new_beams.add((nr, c))

        # Using a set merges beams that land in the same cell,
        # which matches the “dumping into the same place” behavior.
        beams = new_beams

    return split_count

def count_timelines(grid: list[str]) -> int:
    height = len(grid)
    width = len(grid[0])
    start_row, start_col = find_start(grid)

    @lru_cache(maxsize=None)
    def dp(r: int, c: int) -> int:
        # Outside manifold: one completed timeline
        if r < 0 or r >= height or c < 0 or c >= width:
            return 1

        cell = grid[r][c]

        if cell in (".", "S"):
            # Just go straight down
            return dp(r + 1, c)
        elif cell == "^":
            # Split into two timelines: down-left and down-right
            return dp(r + 1, c - 1) + dp(r + 1, c + 1)
        else:
            # Treat unknown chars as empty
            return dp(r + 1, c)

    return dp(start_row, start_col)


def main():
    grid = read_grid("day7_data.txt")
    result_1 = count_splits(grid)
    print(result_1)
    result_2 = count_timelines(grid)
    print(result_2)


if __name__ == "__main__":
    main()