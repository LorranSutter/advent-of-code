import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    patterns, designs = read_file()
    print(patterns)
    print(designs)

    count = 0
    for design in designs:
        print("here1", design)
        # if is_design_possible(design, patterns, design == "bwurrg"):
        if is_design_possible_3(design, patterns):
            count += 1
            print(design, count)
        # print(patterns)
        # input()
        print()

    print("Possible designs:", count)


def part2():
    pass


def read_file():
    patterns = ()
    designs = []
    with open(abs_file_path) as f:
        patterns = tuple(p.strip(" ") for p in f.readline().rstrip("\n").split(","))
        f.readline()

        for line in f:
            designs.append(line.rstrip("\n"))

    return patterns, designs


# def is_design_possible(design, patterns, pause):
#     for pattern in patterns:
#         if pause:
#             print(design, pattern)
#             input()
#         if design.startswith(pattern):
#             size = len(pattern)
#             if pause:
#                 print(size, design[size:])
#                 input()
#             if len(design) == size:
#                 return True
#             return is_design_possible(design[size:], patterns, pause)
#     return False


# def is_design_possible_2(design, patterns):
#     print(design)
#     # input()
#     if not design:
#         return True

#     size = len(design)

#     for i in range(1, size+1):
#         prefix = design[:i]
#         print(i, prefix)

#         if prefix in patterns and is_design_possible_2(design[i:], patterns):
#             return True
#     return False

def is_design_possible_3(design, patterns):
    # print(design)
    # input()
    if not design:
        return True

    size = len(design)

    for i in range(size):
        # print(design[:i+1])
        if design[:i+1] in patterns:
            if i == len(design)-1:
                return True
            if is_design_possible_3(design[i+1:], patterns):
                return True
    return False

part1()
