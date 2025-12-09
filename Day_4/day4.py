from pathlib import Path

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


def read_grid(path: str) -> list[str]:
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]


def find_accessible_positions(grid: list[str]) -> list[tuple[int, int]]:
    rows = len(grid)
    cols = len(grid[0])
    result = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "@":
                continue

            neighbours = 0
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == "@":
                        neighbours += 1

            if neighbours < 4:
                result.append((r, c))

    return result


def remove_positions(grid: list[str], positions: list[tuple[int, int]]) -> list[str]:
    new = [list(row) for row in grid]
    for r, c in positions:
        new[r][c] = "."
    return ["".join(row) for row in new]


def total_removed_rolls(grid: list[str]) -> int:
    total = 0
    current = grid

    while True:
        accessible = find_accessible_positions(current)
        if not accessible:
            break

        total += len(accessible)
        current = remove_positions(current, accessible)

    return total


# ----------- ENTRY POINTS -----------

def solve_part1(grid):
    return len(find_accessible_positions(grid))


def solve_part2(grid):
    return total_removed_rolls(grid)


if __name__ == "__main__":
    data_path = Path(__file__).parent / "day4_data.txt"

    if not data_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {data_path}\n"
            "Make sure you're running the script from inside the Day_4 folder "
            "or that the file exists next to the script."
        )

    grid = read_grid(data_path)
    print("Part 1:", solve_part1(grid))
    print("Part 2:", solve_part2(grid))