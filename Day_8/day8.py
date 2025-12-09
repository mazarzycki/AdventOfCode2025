from pathlib import Path
from collections import Counter


def read_points(filename: str = "day8_data.txt"):
    """Read 3D points from file: each line is 'x,y,z'."""
    data_path = Path(__file__).parent / filename
    if not data_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {data_path!s}.\n"
            "Make sure you're running the script from the project root "
            "or that the file exists in the Day_8 folder."
        )

    points = []
    with data_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y, z = map(int, line.split(","))
            points.append((x, y, z))
    return points


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        # path compression
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        # union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


def build_sorted_edges(points):
    """Return list of (dist2, i, j) sorted by dist2 ascending."""
    n = len(points)
    edges = []
    for i in range(n):
        x1, y1, z1 = points[i]
        for j in range(i + 1, n):
            x2, y2, z2 = points[j]
            dx = x1 - x2
            dy = y1 - y2
            dz = z1 - z2
            dist2 = dx * dx + dy * dy + dz * dz
            edges.append((dist2, i, j))

    edges.sort(key=lambda e: e[0])
    return edges


def solve_k_connections(points, k: int = 1000) -> int:
    n = len(points)
    edges = build_sorted_edges(points)
    uf = UnionFind(n)

    # Connect the k closest distinct pairs
    num_connections = min(k, len(edges))
    for dist2, i, j in edges[:num_connections]:
        uf.union(i, j)

    # Count component sizes
    roots = [uf.find(i) for i in range(n)]
    counts = Counter(roots)
    sizes = sorted(counts.values(), reverse=True)

    if len(sizes) < 3:
        raise ValueError("Less than 3 circuits – unexpected for the puzzle input.")

    a, b, c = sizes[0], sizes[1], sizes[2]
    return a * b * c

def find_last_connection_x_product(points) -> int:
    """
    Continue connecting junction boxes in order of distance until
    all are in one connected component. Return the product of the
    X coordinates of the last two boxes that needed to be connected.
    """
    n = len(points)
    edges = build_sorted_edges(points)
    uf = UnionFind(n)
    components = n

    for dist2, i, j in edges:
        # Find current roots
        ri = uf.find(i)
        rj = uf.find(j)

        # If they're already in the same circuit, this connection
        # doesn't change the number of circuits.
        if ri == rj:
            continue

        # This edge actually merges two circuits
        uf.union(ri, rj)
        components -= 1

        # First time everything is in one circuit
        if components == 1:
            x1 = points[i][0]
            x2 = points[j][0]
            return x1 * x2

    raise RuntimeError("Never reached a single circuit – input might be malformed.")


if __name__ == "__main__":
    points = read_points("day8_data.txt")

    # Part 1 (if you still want to run it)
    part1_result = solve_k_connections(points, k=1000)
    print("Part 1:", part1_result)

    # Part 2
    part2_result = find_last_connection_x_product(points)
    print("Part 2:", part2_result)

