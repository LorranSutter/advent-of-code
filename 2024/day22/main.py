import os
import collections

from utils.timer import timer

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    secrets = read_file()
    it = 2000

    s = 0
    for secret in secrets:
        for _ in range(it):
            # secret = (secret << 6 ^ secret) % 16777216
            # secret = (secret >> 5 ^ secret)
            # secret = (secret << 11 ^ secret) % 16777216
            secret ^= secret * 64 % 16777216
            secret ^= secret // 32  # No prune, always less than 16777216
            secret ^= secret * 2048 % 16777216
        s += secret

    print("Sum", s)


@timer
def part2():
    secrets = read_file()
    it = 2000

    sequences = collections.defaultdict(lambda: 0)
    for secret in secrets:
        seen_seq = set()
        sequence = (10, 10, 10, 10)
        for _ in range(it):
            previous = secret % 10

            secret ^= secret * 64 % 16777216
            secret ^= secret // 32  # No prune, always less than 16777216
            secret ^= secret * 2048 % 16777216

            sequence = sequence[1:] + (secret % 10 - previous,)

            if sequence[0] != 10 and sequence not in seen_seq:
                seen_seq.add(sequence)
                sequences[sequence] += secret % 10

    print("Max bananas", max(sequences.values()))


def read_file():
    secrets = ()
    with open(abs_file_path) as f:
        secrets = (int(num) for num in f.read().split("\n"))

    return secrets


part2()
