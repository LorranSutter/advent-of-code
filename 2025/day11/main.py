import os
from typing import List, Dict

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
Explanation
"""


def part1():
    devices = parse_file()

    count_paths = dfs_count_paths(devices, "you", "out")

    print("Total paths:", count_paths)


def part2():
    # TODO: Implement part 2
    # It is solved, just have to comment out
    devices = parse_file()

    count_paths = 1
    source = "svr"
    for destination in ["fft", "dac", "out"]:
        count_paths *= dfs_count_paths(devices, dict(), source, destination)
        print(f"{source} to {destination}: {count_paths}")
        source = destination

    print("Total paths:", count_paths)

    count_paths = 1
    source = "svr"
    for nodes in [
        ["svr", "fft"],
        # ["svr", "dac"],
        ["fft", "dac"],
        # ["dac", "fft"],
        # ["fft", "out"],
        ["dac", "out"],
    ]:
        count_paths *= dfs_count_paths(devices, dict(), nodes[0], nodes[1])
        print(f"{nodes[0]} to {nodes[1]}: {count_paths}")

    print("Total paths:", count_paths)


def dfs_count_paths(
    devices: Dict[str, List[str]], memo: Dict[str, bool], device: str, destination: str
) -> int:
    if device in memo.keys():
        return memo[device]
    if device == destination:
        return 1
    if device not in devices.keys():
        return 0

    count_paths = 0
    for output in devices[device]:
        count_paths += dfs_count_paths(devices, memo, output, destination)

    memo[device] = count_paths
    return count_paths


def parse_file() -> Dict[str, List[str]]:
    devices = dict()
    with open(abs_file_path) as f:
        for line in f:
            device, outputs = line.strip().split(":")
            outputs = list(outputs.split())

            devices[device] = outputs

    return devices


part2()
