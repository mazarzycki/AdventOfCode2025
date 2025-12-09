from pathlib import Path


def read_and_clean_data():
    data_path = Path(__file__).parent / "day2_data.txt"
    if not data_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {data_path!s}.\nMake sure you're running the script from the project root or that the file exists in the `Day_2` folder."
        )

    with data_path.open("r", encoding="utf-8") as f:
        ranges = f.readlines()
        ranges = [item.strip() for item in ranges]
        return ranges


def calculate_ids(ranges):
    ids = []
    for r in ranges:
        range_pairs = r.split(",")
        for pair in range_pairs:
            for n in range(int(pair.split("-")[0]), int(pair.split("-")[-1]) + 1):
                s = str(n)
                if len(s) % 2 == 0:
                    if s[: len(s) // 2] == s[len(s) // 2 :]:
                        ids.append(n)

    return sum(ids)


def calculate_more_ids(ranges):
    ids = []
    for r in ranges:
        range_pairs = r.split(",")
        for pair in range_pairs:
            start, end = map(int, pair.split("-"))
            for n in range(start, end + 1):
                s = str(n)
                L = len(s)

                for p in range(1, L // 2 + 1):
                    if L % p != 0:
                        continue
                    pattern = s[:p]
                    k = L // p
                    if k >= 2 and pattern * k == s:
                        ids.append(n)

                        break  # no need to try other p

                # if not found: do nothing, n is valid

    return sum(ids)


if __name__ == "__main__":
    id_ranges = read_and_clean_data()
    print(
        "Part 1: sum of all IDs that contain a double letter:", calculate_ids(id_ranges)
    )
    print(
        "Part 2: sum of all IDs that contain a double letter:",
        calculate_more_ids(id_ranges),
    )
