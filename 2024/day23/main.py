import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    adjacent_matrix = read_file()
    cycles = dummy_cycle_3(adjacent_matrix)

    print("Cycles with t", len(cycles))


def part2():
    adjacent_matrix = read_file()
    largest_clique = get_largest_clique(adjacent_matrix)

    print("Password", ",".join(sorted(largest_clique)))


def read_file():
    adjacent_matrix = {}
    with open(abs_file_path) as f:
        for line in f:
            comp1, comp2 = line.rstrip("\n").split("-")
            if comp1 in adjacent_matrix:
                adjacent_matrix[comp1].append(comp2)
            else:
                adjacent_matrix[comp1] = [comp2]

            if comp2 in adjacent_matrix:
                adjacent_matrix[comp2].append(comp1)
            else:
                adjacent_matrix[comp2] = [comp1]

    return adjacent_matrix


def dummy_cycle_3(adjacent_matrix):
    unique_3_cycles = set()
    for vertex in adjacent_matrix.keys():
        for adj1 in adjacent_matrix[vertex]:
            for adj2 in adjacent_matrix[adj1]:
                if vertex in adjacent_matrix[adj2]:
                    if "t" in (vertex[0], adj1[0], adj2[0]):
                        unique_3_cycles.add(tuple(sorted((vertex, adj1, adj2))))

    return unique_3_cycles


def get_largest_clique(adjacent_matrix):
    largest_clique = set()
    for vertex in adjacent_matrix.keys():
        temp_clique = set([vertex])
        for w in adjacent_matrix[vertex]:
            if set(temp_clique) & set(adjacent_matrix[w]) == temp_clique:
                temp_clique.add(w)

        if len(temp_clique) > len(largest_clique):
            largest_clique = temp_clique

    return largest_clique


part2()
