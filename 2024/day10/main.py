import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    topo_map, starts, ends = generate_topo_map_with_borders()

    s = 0
    for start in starts:
        ends_visited = {end: False for end in ends}
        s += score_trailhead(topo_map, start[0], start[1], -1, 0, ends_visited)

    print("Sum of tailhead scores:", s)


def part2():
    topo_map, starts, _ = generate_topo_map_with_borders()

    s = 0
    for start in starts:
        s += score_trailhead_2(topo_map, start[0], start[1], -1, 0)

    print("Sum of tailhead scores:", s)


def generate_topo_map_with_borders():
    '''
    -1 -1 -1 -1
    -1  0  1 -1
    ...
    -1  9  8 -1
    -1 -1 -1 -1
    '''
    m = []
    starts = []
    ends = []
    with open(abs_file_path) as f:
        for i, row in enumerate(f):
            row = [int(digit) for digit in row.rstrip("\n")]
            new_map_row = [-1]
            for j, height in enumerate(row):
                new_map_row.append(height)
                if height == 0:
                    starts.append((i + 1, j + 1))
                elif height == 9:
                    ends.append((i + 1, j + 1))
            m.append(new_map_row + [-1])

    size = len(m[0])
    border = [-1 for _ in range(size)]
    m.insert(0, border)
    m.append(border)

    return m, starts, ends


def score_trailhead(topo_map, i, j, previous_height, score, ends_visited):
    current_height = topo_map[i][j]
    # Out of bounds
    if current_height < 0:
        return score
    if current_height == previous_height + 1:
        if current_height == 9:
            if not ends_visited[(i, j)]:
                ends_visited[(i, j)] = True
                return score + 1
            return score
        else:
            return (
                score
                + score_trailhead(
                    topo_map, i + 1, j, current_height, score, ends_visited
                )
                + score_trailhead(
                    topo_map, i, j + 1, current_height, score, ends_visited
                )
                + score_trailhead(
                    topo_map, i - 1, j, current_height, score, ends_visited
                )
                + score_trailhead(
                    topo_map, i, j - 1, current_height, score, ends_visited
                )
            )
    return score


def score_trailhead_2(topo_map, i, j, previous_height, score):
    current_height = topo_map[i][j]
    # Out of bounds
    if current_height < 0:
        return score
    if current_height == previous_height + 1:
        if current_height == 9:
            return score + 1
        else:
            return (
                score
                + score_trailhead_2(topo_map, i + 1, j, current_height, score)
                + score_trailhead_2(topo_map, i, j + 1, current_height, score)
                + score_trailhead_2(topo_map, i - 1, j, current_height, score)
                + score_trailhead_2(topo_map, i, j - 1, current_height, score)
            )
    return score


part2()
