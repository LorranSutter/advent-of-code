import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    with open(abs_file_path) as f:
        matrix = []
        for line in f:
            matrix.append(line.rstrip("\n"))
        size = len(matrix)

        xmas_count = 0
        for i in range(size):
            for j in range(size):
                if matrix[i][j] == "X":
                    xmas_count += findXmas(matrix, i, j, size)

    print("Total XMAS:", xmas_count)


def part2():
    with open(abs_file_path) as f:
        matrix = []
        for line in f:
            matrix.append(line.rstrip("\n"))
        size = len(matrix)

        xmas_count = 0
        for i in range(size):
            for j in range(size):
                if matrix[i][j] == "A":
                    xmas_count += findMas(matrix, i, j, size)

    print("Total XMAS:", xmas_count)


def findXmas(matrix, i, j, size):
    count = 0
    print(i, j)
    # Horizontal ->
    count += matrix[i][j : j + 4] == "XMAS"
    print(count)
    # Horizontal <-
    count += matrix[i][j - 3 : j + 1] == "SAMX"
    print(count)
    # Vertical \/
    count += "".join([matrix[i + k][j] for k in range(4) if i + k < size]) == "XMAS"
    print(count)
    # Vertical /\
    count += "".join([matrix[i - k][j] for k in range(4) if 0 <= i - k]) == "XMAS"
    print(count)
    # Diagonal --\/
    count += (
        "".join(
            [matrix[i + k][j + k] for k in range(4) if i + k < size and j + k < size]
        )
        == "XMAS"
    )
    print(count)
    # Diagonal --/\
    count += (
        "".join([matrix[i + k][j - k] for k in range(4) if i + k < size and 0 <= j - k])
        == "XMAS"
    )
    print(count)
    # Diagonal \/--
    count += (
        "".join([matrix[i - k][j + k] for k in range(4) if 0 <= i - k and j + k < size])
        == "XMAS"
    )
    # Diagonal /\--
    count += (
        "".join([matrix[i - k][j - k] for k in range(4) if 0 <= i - k and 0 <= j - k])
        == "XMAS"
    )
    print(count)

    return count


def findMas(matrix, i, j, size):
    if i - 1 >= 0 and i + 1 < size and j - 1 >= 0 and j + 1 < size:
        # M.S
        # .A.
        # M.S
        if (
            matrix[i - 1][j - 1] == "M"
            and matrix[i + 1][j - 1] == "M"
            and matrix[i - 1][j + 1] == "S"
            and matrix[i + 1][j + 1] == "S"
        ):
            return 1
        # S.M
        # .A.
        # S.M
        if (
            matrix[i - 1][j - 1] == "S"
            and matrix[i + 1][j - 1] == "S"
            and matrix[i - 1][j + 1] == "M"
            and matrix[i + 1][j + 1] == "M"
        ):
            return 1
        # M.M
        # .A.
        # S.S
        if (
            matrix[i - 1][j - 1] == "M"
            and matrix[i + 1][j - 1] == "S"
            and matrix[i - 1][j + 1] == "M"
            and matrix[i + 1][j + 1] == "S"
        ):
            return 1
        # S.S
        # .A.
        # M.M
        if (
            matrix[i - 1][j - 1] == "S"
            and matrix[i + 1][j - 1] == "M"
            and matrix[i - 1][j + 1] == "S"
            and matrix[i + 1][j + 1] == "M"
        ):
            return 1
    return 0


part2()
