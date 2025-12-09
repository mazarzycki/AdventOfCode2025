from pathlib import Path


def read_and_clean_data():
    data_path = Path(__file__).parent / "day3_data.txt"
    if not data_path.exists():
        raise FileNotFoundError(
            f"Data file not found: {data_path!s}.\n"
            "Make sure you're running the script from the project root or that the file exists in the `Day_3` folder."
        )

    with data_path.open("r", encoding="utf-8") as f:
        batteries = f.readlines()
        batteries = [item.strip() for item in batteries if item.strip()]
        return batteries


def max_joltage_for_bank(bank: str) -> int:
    max_val = -1
    n = len(bank)

    for i in range(n):
        first_digit = int(bank[i])
        for j in range(i + 1, n):
            second_digit = int(bank[j])
            val = first_digit * 10 + second_digit
            if val > max_val:
                max_val = val

    return max_val


def calculate_joltage_differences(batteries):
    total = 0
    for bank in batteries:
        total += max_joltage_for_bank(bank)

    print(total)
    return total

def max_joltage_12_for_bank(bank: str, k: int = 12) -> int:
    L = len(bank)
    assert L >= k, f"Bank too short: length {L}, need {k}"

    result_digits = []
    start = 0
    remaining = k

    while remaining > 0:
        end = L - remaining
        best_digit = "-1"
        best_pos = None

        for i in range(start, end + 1):
            d = bank[i]
            if d > best_digit:
                best_digit = d
                best_pos = i
                if best_digit == "9":
                    break

        result_digits.append(best_digit)
        start = best_pos + 1
        remaining -= 1

    return int("".join(result_digits))


def total_output_joltage_part2(batteries):
    total = 0
    for bank in batteries:
        total += max_joltage_12_for_bank(bank)
    print(total)
    return total


if __name__ == "__main__":
    battery_data = read_and_clean_data()
    final_result = calculate_joltage_differences(battery_data)
    final_resul2 = total_output_joltage_part2(battery_data)
