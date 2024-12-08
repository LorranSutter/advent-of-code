import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    antennas, size = get_antennas_map()
    antinodes = []

    print(size)
    for antenna_type in antennas:
        update_antinodes(antennas[antenna_type], antinodes, False, size)
    antinodes = filter_antinotes(antinodes, size)

    print("Unique antinode locations:", len(antinodes))


def part2():
    antennas, size = get_antennas_map()
    antinodes = []

    print(size)
    for antenna_type in antennas:
        antinodes.extend(antennas[antenna_type])
        update_antinodes(antennas[antenna_type], antinodes, True, size)
    print(antinodes)
    print(len(antinodes))
    antinodes = filter_antinotes(antinodes, size)
    print(antinodes)

    print("Unique antinode locations:", len(antinodes))


def get_antennas_map():
    antennas = {}
    size = 0
    with open(abs_file_path) as f:
        for i, row in enumerate(f):
            size += 1
            for j, item in enumerate(map(str, row.rstrip("\n"))):
                if item != ".":
                    if item not in antennas:
                        antennas[item] = [(i, j)]
                    else:
                        antennas[item].append((i, j))
    return antennas, size


def update_antinodes(antenna_coords, antinodes, extended, size):
    num_coords = len(antenna_coords)
    for i in range(num_coords - 1):
        for j in range(i + 1, num_coords):
            antinodes.extend(
                get_antinodes(antenna_coords[i], antenna_coords[j], extended, size)
            )
            print("total so far", antinodes, len(antinodes))


def get_antinodes(antenna1, antenna2, extended, size):
    distX = antenna2[0] - antenna1[0]
    distY = antenna2[1] - antenna1[1]
    print(antenna1, antenna2)

    antinodes = [
        (antenna1[0] - distX, antenna1[1] - distY),
        (
            antenna2[0] + distX,
            antenna2[1] + distY,
        ),
    ]

    if not extended:
        return antinodes

    multiplier = 2
    while True:
        new_antinode1 = (
            antenna1[0] - distX * multiplier,
            antenna1[1] - distY * multiplier,
        )
        in_bounds1 = in_bounds(new_antinode1, size)

        new_antinode2 = (
            antenna2[0] + distX * multiplier,
            antenna2[1] + distY * multiplier,
        )
        in_bounds2 = in_bounds(new_antinode2, size)

        if in_bounds1:
            antinodes.append(new_antinode1)
        if in_bounds2:
            antinodes.append(new_antinode2)
        if not in_bounds1 and not in_bounds2:
            break

        print(antinodes)
        multiplier += 1

    return antinodes


def filter_antinotes(antinodes, size):
    antinodes = list(set(antinodes))

    filtered_antinodes = []
    for i in range(len(antinodes)):
        if in_bounds(antinodes[i], size):
            filtered_antinodes.append(antinodes[i])

    return filtered_antinodes


def in_bounds(pos, size):
    return pos[0] >= 0 and pos[0] < size and pos[1] >= 0 and pos[1] < size


part2()
