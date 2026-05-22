import math
from typing import List, Tuple


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\x1b[6;30;42m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


class tcolors:
    BLACK = "\33[30m"
    RED = "\33[31m"
    GREEN = "\33[32m"
    YELLOW = "\33[33m"
    BLUE = "\33[34m"
    VIOLET = "\33[35m"
    BEIGE = "\33[36m"
    WHITE = "\33[37m"
    RESET = "\033[0m"


def add(v1: List[int] | Tuple[int], v2: List[int] | Tuple[int]):
    return (v1[0] + v2[0], v1[1] + v2[1])


def sub(v1: List[int] | Tuple[int], v2: List[int] | Tuple[int]):
    return (v1[0] - v2[0], v1[1] - v2[1])


def mul(a, v: List[int] | Tuple[int]):
    return (a * v[0], a * v[1])


def mod(v1: List[int] | Tuple[int], v2: List[int] | Tuple[int]):
    return (v1[0] % v2[0], v1[1] % v2[1])


def dist(v1: List[int] | Tuple[int], v2: List[int] | Tuple[int]):
    a, b = v2[0] - v1[0], v2[1] - v1[1]
    return math.sqrt(a * a + b * b)


def dist3(v1: List[int] | Tuple[int], v2: List[int] | Tuple[int]):
    a, b, c = v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]
    return math.sqrt(a * a + b * b + c * c)


def cross(v1: List[int] | Tuple[int], v2: List[int] | Tuple[int]):
    return v1[0] * v2[1] - v2[0] * v1[1]
