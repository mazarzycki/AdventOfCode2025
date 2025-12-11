from pathlib import Path


def read_graph(input_path: str) -> dict[str, list[str]]:
    """
    Parse the input into a directed graph.

    Each line looks like:
        aaa: you hhh
    meaning edges:
        aaa -> you
        aaa -> hhh
    """
    path = Path(__file__).parent / input_path
    graph: dict[str, list[str]] = {}

    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            left, right = line.split(":")
            src = left.strip()
            targets_part = right.strip()

            if targets_part:
                neighbors = targets_part.split()
            else:
                neighbors = []

            graph[src] = neighbors

    return graph


# ---------- Part 1 ----------

def count_paths(graph: dict[str, list[str]], start: str, end: str) -> int:
    """
    Count the number of distinct paths from start to end
    using DFS + memoization.
    """
    memo: dict[str, int] = {}

    def dfs(node: str) -> int:
        if node == end:
            return 1

        if node in memo:
            return memo[node]

        total = 0
        for nxt in graph.get(node, []):
            total += dfs(nxt)

        memo[node] = total
        return total

    return dfs(start)


def solve_part1(input_path: str) -> int:
    graph = read_graph(input_path)
    return count_paths(graph, "you", "out")


# ---------- Part 2 ----------

def count_paths_with_dac_fft(graph: dict[str, list[str]], start: str, end: str) -> int:
    """
    Count how many paths from start to end visit both 'dac' and 'fft'
    (in any order), using DFS + memoization over (node, mask).

    mask bits:
        bit 0 (1): have we visited 'dac' so far?
        bit 1 (2): have we visited 'fft' so far?
    """
    memo: dict[tuple[str, int], int] = {}

    def dfs(node: str, mask: int) -> int:
        # Update mask on arrival
        if node == "dac":
            mask |= 1  # set bit 0
        if node == "fft":
            mask |= 2  # set bit 1

        # If we reached end, count this path only if mask == 3 (both visited)
        if node == end:
            return 1 if mask == 3 else 0

        key = (node, mask)
        if key in memo:
            return memo[key]

        total = 0
        for nxt in graph.get(node, []):
            total += dfs(nxt, mask)

        memo[key] = total
        return total

    # Start with mask = 0 (haven't seen dac or fft yet)
    return dfs(start, 0)


def solve_part2(input_path: str) -> int:
    graph = read_graph(input_path)

    # Optional: if you also want the *total* number of paths svr -> out
    total_paths = count_paths(graph, "svr", "out")

    good_paths = count_paths_with_dac_fft(graph, "svr", "out")

    print(f"Total paths from svr to out: {total_paths}")
    print(f"Paths that visit both dac and fft: {good_paths}")

    return good_paths


# ---------- Main ----------

if __name__ == "__main__":
    INPUT_FILE = "day11_data.txt"  

    part1 = solve_part1(INPUT_FILE)
    print("Part 1:", part1)

    part2 = solve_part2(INPUT_FILE)
    print("Part 2:", part2)
