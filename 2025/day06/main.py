import os
from typing import List, Tuple

from utils.timer import timer

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
Part 1:
- We read the input file and parse it separating the numbers and operations.
- So we have something like:
    nums = [
            (1, 2, 3),
            (4, 5, 6),
            (7, 8, 9)
            ]
    ops = ['+', '*', '+']
- Then we iterate over the operations, and for each operation we iterate over the columns of numbers.
- We apply the operation accordingly to the column and add the result to the grand total.

Part 2:
- For this part we read the input file, but don't split the numbers, since the empty spaces are significant.
- So we have something like:
    rows = [
            "123 328  51 64 ",
            " 45 64  387 23 ",
            "  6 98  215 314"
            ]
    ops = ['*', '+', '*', '+']
- We know that all rows have the same length, so we can iterate over the columns.
- We concatenate each column until a column is completly empty (only spaces), summing or multiplying the result depending on the operation.
- When we reach an empty column, we move to the next operation.
- Finally, we add the result to the grand total.
"""


@timer
def part1():
    nums, ops = parse_file_1()
    len_col = len(nums)

    grant_total = 0
    for i in range(len(ops)):
        if ops[i] == "+":
            for j in range(len_col):
                grant_total += nums[j][i]
        else:
            prod = 1
            for j in range(len_col):
                prod *= nums[j][i]
            grant_total += prod

    print("Grand total", grant_total)


@timer
def part2():
    rows, ops = parse_file_2()
    grant_total = 0

    op_id = 0
    op = ops[op_id]
    col_result = 0 if op == "+" else 1
    for i in range(len(rows[0])):
        num = ""
        for row in rows:
            num += row[i]
        if num.strip().isnumeric():
            if op == "+":
                col_result += int(num)
            else:
                col_result *= int(num)
        else:
            # If the col_result is not numeric, it means we reached an empty column
            grant_total += col_result
            op_id += 1
            op = ops[op_id]
            col_result = 0 if op == "+" else 1

    print("Grand total", grant_total + col_result)


def parse_file_1() -> Tuple[List[Tuple[int]], List[str]]:
    nums, ops = [], []
    with open(abs_file_path) as f:
        for line in f:
            line = line.strip().split()
            if line[0].isnumeric():
                nums.append(tuple(map(int, line)))
            else:
                ops = line

    return nums, ops


def parse_file_2() -> Tuple[List[Tuple[str]], List[str]]:
    rows, ops = [], []
    with open(abs_file_path) as f:
        for line in f:
            if line[0] in ("*", "+"):
                ops = line.strip().split()
            else:
                # :-1 to remove \n
                rows.append(line[:-1])

    return rows, ops


part2()
