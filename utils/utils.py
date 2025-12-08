import math
from typing import List, Tuple


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

def cross(v1: List[int] | Tuple[int],v2: List[int] | Tuple[int]):
    return v1[0]*v2[1] - v2[0]*v1[1]