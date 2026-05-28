import os
from typing import List, Dict

from utils.timer import timer
from utils.utils import tcolors

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)

"""
Preprocessing:
- Read the input file and parse it into a dictionary (adjacency list) representing the device network

Part 1:
- This problem can be modeled as a graph problem where we need to find all possible paths between two nodes
- We use a simple Depth-First Search (DFS) approach to solve it
- Starting at the source node ("you"), we recursively explore all adjacent nodes until we reach the destination ("out")
- When we find the destination, we return 1 (representing one valid path); if we reach a dead end, we return 0
- The recursive calls sum up all the paths found through each branch
- By the end of the recursion, we have the total count of all possible paths from source to destination

Part 2:
- The key insight is that we can break this problem into subparts
- Since we need paths that pass through both "fft" and "dac", we can apply a similar DFS approach to each segment:
  svr → fft, fft → dac, and dac → out
- Once we have the number of possible paths for each segment, the final result is simply the product of all subproblems
- This works because each path through the first segment can combine with each path through the second segment, and so on
- However, due to the large input size, an ordinary DFS would be impractical to finish in reasonable time
- We apply memoization to cache results and avoid recalculating paths for the same device multiple times
"""


@timer
def part1():
    devices = parse_file()

    count_paths = dfs_count_paths(devices, "you", "out")

    print("Total paths:", count_paths)


@timer
def part2():
    devices = parse_file()

    count_paths = 1
    source = "svr"
    for destination in ["fft", "dac", "out"]:
        paths = dfs_count_paths_memo(devices, dict(), source, destination)
        count_paths *= paths
        print(
            f"Paths from {tcolors.GREEN}{source}{tcolors.RESET} to {tcolors.RED}{destination}{tcolors.RESET}: {tcolors.YELLOW}{paths}{tcolors.RESET}"
        )
        source = destination

    print("Total paths:", count_paths)


def dfs_count_paths(
    devices: Dict[str, List[str]], device: str, destination: str
) -> int:
    if device == destination:
        return 1
    if device not in devices.keys():
        return 0

    count_paths = 0
    for output in devices[device]:
        count_paths += dfs_count_paths(devices, output, destination)

    return count_paths


def dfs_count_paths_memo(
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
        count_paths += dfs_count_paths_memo(devices, memo, output, destination)

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


part1()
part2()
