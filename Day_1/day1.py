from pathlib import Path


def read_and_clean_data():
    data_path = Path(__file__).parent / "day1_data.txt"
    if not data_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {data_path!s}.\nMake sure you're running the script from the project root or that the file exists in the `Day_1` folder."
        )

    with data_path.open("r", encoding="utf-8") as f:
        rotations = f.readlines()
        rotations = [item.strip() for item in rotations]
        return rotations


def calculate_zeros(rotations):
    print(rotations)
    start_value = 50
    values = []
    for value in rotations:
        if value[0] == "R":
            start_value += int(value[1:])
            start_value = start_value % 100
            values.append(start_value)
        elif value[0] == "L":
            start_value -= int(value[1:])
            start_value = start_value % 100
            values.append(start_value)
    final_value = values.count(0)
    print(f"Final count of zeros: {final_value}")
    return final_value

def zeros_hit_from(start, step, modulo=100):
    """
    start: current dial position (0-99)
    step:  >0 for R, <0 for L
    returns: how many times we land exactly on 0 during this rotation
    """
    if step == 0:
        return 0

    m = modulo
    d = abs(step)

    if step > 0:
        # moving right: 0 reached after (100 - start) clicks (except start=0)
        first = (m - start) % m
    else:
        # moving left: 0 reached after `start` clicks (except start=0)
        first = start % m

    # if we start at 0, the next time we hit 0 is after a full turn (100 steps)
    if first == 0:
        first = m

    # not enough distance to reach 0 even once
    if d < first:
        return 0

    # first hit at `first`, then every +100 steps
    return 1 + (d - first) // m


def calculate_zero_events(rotations):
    pos = 50
    zeros_at_end = 0  # times we end a rotation at 0
    zeros_all_clicks = 0  # times we hit 0 during *any* click

    for token in rotations:
        direction = token[0]
        amount = int(token[1:])

        step = amount if direction == "R" else -amount

        # count all zero hits during this rotation
        zeros_all_clicks += zeros_hit_from(pos, step)

        # move and wrap
        pos = (pos + step) % 100

        # part 1: end-of-rotation zero
        if pos == 0:
            zeros_at_end += 1

    return zeros_at_end, zeros_all_clicks


if __name__ == "__main__":
    rotations = read_and_clean_data()

    # Part 1 (your original logic)
    zeros_end_only = calculate_zeros(rotations)

    # Part 2 (method 0x434C49434B)
    zeros_at_end, zeros_all_clicks = calculate_zero_events(rotations)

    print("Check – zeros at end (from new function):", zeros_at_end)
    print("Part 2 – total times dial points at 0 (during + at end):", zeros_all_clicks)

    # If you explicitly want:
    # "sum of zeros at the end + times it crosses 0 in-between"
    zeros_during_only = zeros_all_clicks - zeros_at_end
    print("Zeros during rotations only (excluding ends):", zeros_during_only)
    print("Sum (end zeros + during zeros):", zeros_all_clicks)  # same as part 2
