from pathlib import Path
from itertools import combinations
from collections import deque


def read_points(path: Path):
    points = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x_str, y_str = line.split(",")
            points.append((int(x_str), int(y_str)))
    return points


# ---------- Part 1 ----------


def largest_rectangle_area_part1(points):
    max_area = 0
    for (x1, y1), (x2, y2) in combinations(points, 2):
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        area = (dx + 1) * (dy + 1)
        if area > max_area:
            max_area = area
    return max_area


# ---------- Part 2 helpers ----------


def build_allowed_tiles(points):
    """
    Given the ordered list of red points that form a loop,
    return a set of all tiles that are red or green.

    Strategy:
    - Build the boundary loop (red + green tiles along each segment).
    - Flood-fill from outside to mark outside tiles.
    - Anything not outside and not boundary is interior (green).
    """
    n = len(points)
    if n == 0:
        return set()

    boundary = set()

    # 1) Build boundary tiles: connect each pair of consecutive red points (wrap around)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]

        if x1 == x2:
            # vertical segment
            step = 1 if y2 >= y1 else -1
            for y in range(y1, y2 + step, step):
                boundary.add((x1, y))
        elif y1 == y2:
            # horizontal segment
            step = 1 if x2 >= x1 else -1
            for x in range(x1, x2 + step, step):
                boundary.add((x, y1))
        else:
            # Problem statement guarantees same row or column
            raise ValueError(
                f"Non-axis-aligned segment between {points[i]} and {points[(i + 1) % n]}"
            )

    # Compute bounding box of the loop
    xs = [x for x, _ in boundary]
    ys = [y for _, y in boundary]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # 2) Flood fill from outside to find which tiles are outside the loop
    outside = set()
    start = (min_x - 1, min_y - 1)
    q = deque([start])
    outside.add(start)

    # We consider a slightly expanded bounding box for the flood fill
    low_x, high_x = min_x - 1, max_x + 1
    low_y, high_y = min_y - 1, max_y + 1

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx < low_x or nx > high_x or ny < low_y or ny > high_y:
                continue
            if (nx, ny) in outside:
                continue
            if (nx, ny) in boundary:
                # Can't pass through the loop
                continue
            outside.add((nx, ny))
            q.append((nx, ny))

    # 3) Tiles that are not outside and not boundary
    #    and within the original bounding box are interior (green)
    allowed = set(boundary)  # start with boundary (red + boundary-green)
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) not in outside and (x, y) not in boundary:
                allowed.add((x, y))

    # Also return bbox for later grid construction
    return allowed, (min_x, max_x, min_y, max_y)


def build_prefix_sum(allowed, bbox):
    """
    Build a 2D prefix sum array over the bounding box for fast
    rectangle-all-green checks.

    allowed: set of (x,y) that are red or green
    bbox: (min_x, max_x, min_y, max_y)
    """
    min_x, max_x, min_y, max_y = bbox
    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # grid[row][col] where row corresponds to y, col to x
    grid = [[0] * width for _ in range(height)]

    for x, y in allowed:
        col = x - min_x
        row = y - min_y
        grid[row][col] = 1

    # prefix[r+1][c+1] = sum of grid[0..r][0..c]
    prefix = [[0] * (width + 1) for _ in range(height + 1)]

    for r in range(height):
        row_sum = 0
        for c in range(width):
            row_sum += grid[r][c]
            prefix[r + 1][c + 1] = prefix[r][c + 1] + row_sum

    return prefix, (min_x, min_y)


def rect_sum(prefix, origin, x1, y1, x2, y2):
    """
    Return sum of cells in the rectangle with corners
    (x1, y1) and (x2, y2) inclusive, using the prefix sum.

    origin = (min_x, min_y) of the grid
    """
    min_x, min_y = origin
    # Ensure x1 <= x2 and y1 <= y2
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1

    j1 = x1 - min_x
    j2 = x2 - min_x
    i1 = y1 - min_y
    i2 = y2 - min_y

    # inclusive rectangle
    total = (
        prefix[i2 + 1][j2 + 1]
        - prefix[i1][j2 + 1]
        - prefix[i2 + 1][j1]
        + prefix[i1][j1]
    )
    return total


# ---------- Part 2 ----------


def compress_coordinates(points):
    """
    Given original points [(x, y), ...] in loop order,
    return:
      - points_comp: same points but with compressed integer coords
      - xs: sorted unique original x's
      - ys: sorted unique original y's
    """
    xs = sorted({x for x, _ in points})
    ys = sorted({y for _, y in points})

    x_index = {x: i for i, x in enumerate(xs)}
    y_index = {y: i for i, y in enumerate(ys)}

    points_comp = [(x_index[x], y_index[y]) for x, y in points]
    return points_comp, xs, ys


def largest_rectangle_area_part2(points_orig):
    """
    points_orig: list of (x, y) in original coordinates, in loop order.
    Returns the largest *real* area (in tiles) of any valid rectangle.
    """

    if len(points_orig) < 2:
        return 0

    # 1) Compress coordinates for geometric checks
    points_comp, xs, ys = compress_coordinates(points_orig)

    # 2) Build allowed cells (boundary + interior) on compressed grid
    allowed, bbox = build_allowed_tiles(points_comp)
    prefix, origin = build_prefix_sum(allowed, bbox)

    max_area = 0

    # We'll need both original and compressed coordinates per red tile
    # Keep them aligned by index.
    for i, (x1_orig, y1_orig) in enumerate(points_orig):
        ix1, iy1 = points_comp[i]

        for j in range(i + 1, len(points_orig)):
            x2_orig, y2_orig = points_orig[j]
            ix2, iy2 = points_comp[j]

            # 3) First check validity in COMPRESSED grid:
            #    all compressed cells in this rectangle must be allowed.
            width_cells = abs(ix1 - ix2) + 1
            height_cells = abs(iy1 - iy2) + 1
            cells_in_rect = width_cells * height_cells

            allowed_cells = rect_sum(prefix, origin, ix1, iy1, ix2, iy2)
            if allowed_cells != cells_in_rect:
                continue  # some part of the rectangle is outside red/green region

            # 4) Now compute REAL area in original coordinates
            width_tiles = abs(x1_orig - x2_orig) + 1
            height_tiles = abs(y1_orig - y2_orig) + 1
            area_tiles = width_tiles * height_tiles

            if area_tiles > max_area:
                max_area = area_tiles

    return max_area


def main():
    data_path = Path(__file__).parent / "day9_data.txt"
    if not data_path.exists():
        raise FileNotFoundError(f"Input file not found: {data_path}")

    points = read_points(data_path)  # original coordinates

    part1 = largest_rectangle_area_part1(points)
    print("Part 1:", part1)

    part2 = largest_rectangle_area_part2(points)
    print("Part 2:", part2)


if __name__ == "__main__":
    main()
