coords = ["2,3", "4,0", "-1,5"]

# result [(2, 3), (4, 0), (-1, 5)]

new_coords = [tuple(map(int, coord.split(","))) for coord in coords]

print(new_coords)