import os


script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
Part 1:
I used a naive approach and not optimized for performance.
For each range, I iterate through each ID and check if it is an invalid ID.
I just convert the potential invalid ID to a string and check if the first half is equal to the second half.

Part2:
A bit more optimized approach.
Instead of checking each ID in the ranges, I generate all possible invalid IDs. The last one is the top limit range.

The invalid IDs generation is the interesting part

Invalid ID: 999
We can rewrite 999 as 9*111
Then, 9*1 + 9*10 + 9*100
Writing as power of 10, we get 9*10^0 + 9*10^1 + 9*10^2

For numbers with more than one digit
Invalid ID: 232323
We can rewrite 232323 as 23*1001001
Then, 23*1 + 23*100 + 23*10000
Writing as power of 10, we get 23*10^0 + 23*10^2 + 23*10^4

A general formula is: id * 10^(n*i)
Where n is the number of digits in the ID, and i is the index of the digit.

With that in mind, we can generate all invalid IDs and check if they are in one of the ID ranges.
And we can save some computation with this approach:
- We can stop when the ID length to be tested is greater than the length of the longest ID.
- We just have to generate invalid IDs up to the length of longest_ID_length/current_id_length
  e.g., if current_id_length is 2 and longest_ID_length is 10, we just have to iterate up to i == 5
"""


def part1():
    ids_range = parse_file()
    total = 0

    for ids in ids_range:
        start, end = ids[0], ids[1]
        for id in range(start, end + 1):
            id_str = str(id)
            len_id = len(id_str)
            if len_id % 2 != 0:
                continue
            else:
                if id_str[len_id // 2 :] == id_str[: len_id // 2]:
                    total += id

    print("Sum of invalid IDs:", total)


def part2():
    ids_range = parse_file()

    # Find the length of the longest ID
    max_id = ids_range[0][1]
    for ids in ids_range:
        max_id = max(max_id, ids[1])
    len_max_id = len(str(max_id))

    # Make a set of invalid IDs to avoid including the same ID more than once
    invalid_ids = set()
    for id in range(1, max_id // 2):
        len_id = len(str(id))
        if len_id > len_max_id // 2:
            break

        # We initialize invalid_id with the ID to not check a single number in the ranges
        invalid_id = id
        for i in range(1, len_max_id // len_id):
            invalid_id += id * 10 ** (len_id * i)

            for ids in ids_range:
                if ids[0] <= invalid_id <= ids[1]:
                    invalid_ids.add(invalid_id)

    print("Sum of invalid IDs:", sum(invalid_ids))


def parse_file():
    ids_range = []
    with open(abs_file_path) as f:
        ids_range = f.readline().split(",")
        for i in range(len(ids_range)):
            ids_range[i] = list(map(int, (ids_range[i].strip().split("-"))))

    return ids_range


part2()
