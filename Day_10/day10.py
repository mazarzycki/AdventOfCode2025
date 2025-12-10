from collections import deque
from pathlib import Path
import re

import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds


# ----------------------
# Part 1
# ----------------------


def parse_line(line: str):
    """
    Parse one line like:
    [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

    Returns:
        n: number of lights
        target: bitmask of desired configuration
        button_masks: list of bitmasks, one per button
    """
    line = line.strip()

    # Extract indicator diagram between [ and ]
    start_idx = line.index("[") + 1
    end_idx = line.index("]")
    diagram = line[start_idx:end_idx]
    n = len(diagram)

    # Build target bitmask (# = 1, . = 0)
    target = 0
    for i, ch in enumerate(diagram):
        if ch == "#":
            target |= 1 << i

    # Find all button groups (...) and convert to bitmasks
    button_masks = []
    for group in re.findall(r"\(([^)]*)\)", line):
        group = group.strip()
        if not group:
            continue
        indices = [int(x) for x in group.split(",") if x.strip()]
        mask = 0
        for idx in indices:
            mask |= 1 << idx
        button_masks.append(mask)

    return n, target, button_masks


def min_presses(n: int, target: int, button_masks: list[int]) -> int:
    """
    BFS over states (bitmasks 0..2^n-1) to find the minimum number
    of button presses to reach `target` from all-off (0).
    """
    if target == 0:
        return 0

    max_state = 1 << n
    dist = [-1] * max_state

    q = deque([0])  # start from all lights off
    dist[0] = 0

    while q:
        state = q.popleft()
        d = dist[state]

        for bm in button_masks:
            nxt = state ^ bm  # pressing button toggles these bits
            if dist[nxt] == -1:
                dist[nxt] = d + 1
                if nxt == target:
                    return d + 1  # found shortest path
                q.append(nxt)

    # If the puzzle is well-formed, this shouldn't happen
    raise ValueError("Target configuration unreachable")


def solve_part1(input_path: str | Path) -> int:
    total_presses = 0
    input_path = Path(__file__).parent / input_path

    with input_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n, target, button_masks = parse_line(line)
            presses = min_presses(n, target, button_masks)
            total_presses += presses

    return total_presses


# ----------------------
# Part 2 (ILP with SciPy)
# ----------------------


def parse_line_part2(line: str):
    """
    For part 2 we ignore the indicator lights and use:
      - button wiring (same as before, but we keep index lists)
      - joltage requirements {a,b,c,...}

    Returns:
        targets: list[int] - target value for each counter
        button_indices: list[list[int]] - which counters each button increments
    """
    line = line.strip()

    # Extract joltage requirements between { and }
    m = re.search(r"\{([^}]*)\}", line)
    if not m:
        raise ValueError(f"No joltage requirements found in line: {line!r}")
    targets = [int(x) for x in m.group(1).split(",") if x.strip()]

    # Extract button groups as lists of indices
    button_indices: list[list[int]] = []
    for group in re.findall(r"\(([^)]*)\)", line):
        group = group.strip()
        if not group:
            continue
        indices = [int(x) for x in group.split(",") if x.strip()]
        button_indices.append(indices)

    return targets, button_indices


def min_presses_counters(targets: list[int], button_indices: list[list[int]]) -> int:
    """
    Solve:
        minimize sum_i x_i
        subject to A x = targets
                  x_i >= 0, integer
    where A[j,i] = 1 if button i affects counter j.
    """
    m = len(targets)  # counters
    n = len(button_indices)  # buttons

    # Build A (m x n) matrix
    A = np.zeros((m, n), dtype=float)
    for col, inds in enumerate(button_indices):
        for row in inds:
            A[row, col] = 1.0

    targets_arr = np.array(targets, dtype=float)

    # Objective: minimize sum_i x_i
    c = np.ones(n, dtype=float)

    # All variables must be integers
    integrality = np.ones(n, dtype=int)

    # Bounds: x_i >= 0, no explicit upper bound (solver will find min)
    bounds = Bounds(lb=0, ub=np.inf)

    # Constraints: A x = targets
    constraints = LinearConstraint(A, lb=targets_arr, ub=targets_arr)

    res = milp(
        c=c,
        integrality=integrality,
        bounds=bounds,
        constraints=constraints,
    )

    if not res.success:
        raise ValueError(f"MILP failed to find solution: {res.message}")

    # res.fun is the minimum total presses (float but integer-valued)
    return int(round(res.fun))


def solve_part2(input_path: str | Path) -> int:
    total_presses = 0
    input_path = Path(__file__).parent / input_path

    with input_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            targets, button_indices = parse_line_part2(line)
            presses = min_presses_counters(targets, button_indices)
            total_presses += presses

    return total_presses


# ----------------------
# Main
# ----------------------

if __name__ == "__main__":
    input_file = "day10_data.txt"

    part1 = solve_part1(input_file)
    print("Part 1:", part1)

    part2 = solve_part2(input_file)
    print("Part 2:", part2)
