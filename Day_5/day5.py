from pathlib import Path


def read_and_clean_data():
    data_path_1 = Path(__file__).parent / "day5_fresh.txt"
    data_path_2 = Path(__file__).parent / "day5_ingredients.txt"
    if not data_path_1.exists():
        raise FileNotFoundError(
            f"Data file not found: {data_path_1!s}.\n"
            "Make sure you're running the script from the project root or that the file exists in the `Day_5` folder."
        )
    elif not data_path_2.exists():
        raise FileNotFoundError(
            f"Data file not found: {data_path_2!s}.\n"
            "Make sure you're running the script from the project root or that the file exists in the `Day_5` folder."
        )

    with data_path_1.open("r", encoding="utf-8") as f:
        fresh_list = f.readlines()
        fresh_list = [item.strip() for item in fresh_list if item.strip()]
    
    with data_path_2.open("r", encoding="utf-8") as f:
        ingredients_list = f.readlines()
        ingredients_list = [item.strip() for item in ingredients_list if item.strip()]
    
    return fresh_list, ingredients_list

def find_fresh_ingredients(fresh_list, ingredients_list):
    fresh_ranges = [tuple(map(int, f.split('-'))) for f in fresh_list]
    ingredients = [int(i) for i in ingredients_list]

    fresh_ingredients = 0

    for ingredient in ingredients:
        if any(start <= ingredient <= end for start, end in fresh_ranges):
            fresh_ingredients += 1

    print(f"Found {fresh_ingredients} fresh ingredients.")
    return fresh_ingredients

def ids_considered_fresh(fresh_list):
    """Part 2: count how many distinct IDs are covered by the fresh ranges."""
    ranges = [tuple(map(int, f.split("-"))) for f in fresh_list]

    # 1) sort by start
    ranges.sort(key=lambda x: x[0])

    # 2) merge overlapping/touching ranges
    merged = []
    for start, end in ranges:
        if not merged:
            merged.append([start, end])
        else:
            last_start, last_end = merged[-1]

            # Overlap or touch: extend the last range
            if start <= last_end + 1:
                merged[-1][1] = max(last_end, end)
            else:
                # Disjoint: start a new merged range
                merged.append([start, end])

    # 3) sum lengths of merged ranges (inclusive)
    total_fresh_ids = sum(end - start + 1 for start, end in merged)

    print(f"Part 2: {total_fresh_ids} ingredient IDs are considered fresh.")
    return total_fresh_ids


if __name__ == "__main__":
    fresh_list, ingredients_list = read_and_clean_data()
    find_fresh_ingredients(fresh_list, ingredients_list)  # Part 1
    ids_considered_fresh(fresh_list)                       # Part 2