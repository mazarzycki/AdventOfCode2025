from pathlib import Path
import pandas as pd


def read_and_clean_data_part_1():
    data_path = Path(__file__).parent / "day6_data.txt"
    if not data_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {data_path!s}.\n"
            "Make sure you're running the script from the project root or that the file exists in the `Day_6` folder."
        )
    df = pd.read_csv(
        data_path,
        sep="\s+",  
        header=None,
        engine="python",
    )

    df.columns = range(len(df.columns))
    df.iloc[:-1] = df.iloc[:-1].apply(pd.to_numeric)

    results = []
    for col in df.columns:
        op = df.iloc[-1, col]
        if op == "+":
            results.append(df.iloc[:-1, col].sum())
        elif op == "*":
            results.append(df.iloc[:-1, col].prod())
        else:
            raise ValueError(f"Unexpected operator {op!r} in column {col}")
    final_result = sum(results)
    return final_result

def read_grid_as_dataframe():
    """Reads the file as a full character grid (needed for part 2)."""
    data_path = Path(__file__).parent / "day6_data.txt"
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path!s}")

    with data_path.open() as f:
        lines = [line.rstrip("\n") for line in f]

    # Normalize all lines to same width
    width = max(len(line) for line in lines)
    lines = [line.ljust(width) for line in lines]

    # Convert to DataFrame of characters
    df = pd.DataFrame([list(row) for row in lines])
    return df


def find_blocks(df: pd.DataFrame):
    """Returns list of (start_col, end_col) for each problem block."""
    col_is_empty = (df == " ").all(axis=0)

    blocks = []
    in_block = False
    start = None

    for col, empty in col_is_empty.items():
        if not empty and not in_block:
            in_block = True
            start = col
        elif empty and in_block:
            in_block = False
            blocks.append((start, col - 1))

    if in_block:
        blocks.append((start, df.shape[1] - 1))

    return blocks


def evaluate_block_part2(df: pd.DataFrame, start: int, end: int) -> int:
    """
    Evaluates one block for part 2, where each column inside the block
    represents one number (top-to-bottom digits), and the operator is
    in the bottom row.
    """

    # Operator for the whole block sits somewhere in the bottom row
    op_chunk = "".join(df.iloc[-1, start:end+1])

    if "+" in op_chunk:
        op = "+"
    elif "*" in op_chunk:
        op = "*"
    else:
        raise ValueError(f"No operator found in block {start}-{end}")

    numbers = []

    # Read columns from right to left
    for col in range(end, start - 1, -1):
        col_chars = df.iloc[:-1, col]  # exclude bottom row
        digits = "".join(col_chars).strip()

        if digits:  # skip columns that contain only spaces
            numbers.append(int(digits))

    # Compute block result
    if op == "+":
        return sum(numbers)
    else:
        product = 1
        for n in numbers:
            product *= n
        return product


# ---------------------------------------------------------
# PART 2 LOGIC
# ---------------------------------------------------------

def solve_part2():
    df = read_grid_as_dataframe()
    blocks = find_blocks(df)

    total = 0
    for start, end in blocks:
        total += evaluate_block_part2(df, start, end)

    return total


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

if __name__ == "__main__":
    p1 = read_and_clean_data_part_1()
    print(f"Part 1 result: {p1}")

    p2 = solve_part2()
    print(f"Part 2 result: {p2}")


    
