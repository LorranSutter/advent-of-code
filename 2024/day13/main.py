import os
import re
import math

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    buttons_a, buttons_b, prizes = read_file()

    tokens_spend = 0
    for i in range(len(prizes)):
        _, _, min_cost = minimize_cost_diophantine(
            buttons_a[i], buttons_b[i], 3, 1, prizes[i][0], prizes[i][1]
        )
        if min_cost != math.inf:
            tokens_spend += min_cost

    print("Tokens spend:", tokens_spend)


def part2():
    buttons_a, buttons_b, prizes = read_file()
    shift = 10000000000000

    tokens_spend = 0
    for i in range(len(prizes)):
        prize = (prizes[i][0] + shift, prizes[i][1] + shift)
        _, _, min_cost = minimize_cost_cramer(
            buttons_a[i], buttons_b[i], 3, 1, prize[0], prize[1]
        )
        tokens_spend += min_cost

    print("Tokens spend:", tokens_spend)


def read_file():
    pattern_button_a = r"Button A: X\+(\d+), Y\+(\d+)"
    pattern_button_b = r"Button B: X\+(\d+), Y\+(\d+)"
    pattern_prize = r"Prize: X=(\d+), Y=(\d+)"

    buttons_a = []
    buttons_b = []
    prizes = []
    with open(abs_file_path) as f:
        for line in f:
            if match := re.search(pattern_button_a, line):
                buttons_a.append((int(match.group(1)), int(match.group(2))))
            elif match := re.search(pattern_button_b, line):
                buttons_b.append((int(match.group(1)), int(match.group(2))))
            elif match := re.search(pattern_prize, line):
                prizes.append((int(match.group(1)), int(match.group(2))))

    return buttons_a, buttons_b, prizes


def minimize_cost_diophantine(A, B, cost_A, cost_B, X, Y):
    """
    Diophantine system equations
    For some reason only works for part 1
    """
    max_b = X // B[0] if X > Y else Y // B[1]

    # Try all possible values of b within a reasonable range
    best_cost = math.inf
    best_a, best_b = 0, 0
    for b in range(0, max_b):
        if (X - B[0] * b) % A[0] == 0:
            a = (X - B[0] * b) // A[0]
            if A[1] * a + B[1] * b == Y:  # Verify the second equation
                cost = cost_A * a + cost_B * b
                if cost < best_cost:
                    best_cost = cost
                    best_a, best_b = a, b

    return best_a, best_b, best_cost


def minimize_cost_cramer(A, B, cost_A, cost_B, X, Y):
    """
    Cramer's rule to solve linear system

    // a*A[0] + b*B[0] = X
    \\ b*A[1] + b*B[1] = Y

    det = | A[0] B[0] |
          | A[1] B[1] |

         | X B[0] |
         | Y B[1] |
    a = ------------
            det

         | X A[0] |
         | Y A[1] |
    b = ------------
            det
    """

    det = A[0] * B[1] - A[1] * B[0]

    a = (X * B[1] - B[0] * Y) // det
    b = (A[0] * Y - X * A[1]) // det

    if A[0] * a + B[0] * b == X and A[1] * a + B[1] * b == Y:
        return a, b, cost_A * a + cost_B * b
    return 0, 0, 0


def brute_force(A, B, cost_A, cost_B, X, Y):
    max_b = X // B[0] if X > Y else Y // B[1]

    min_cost = math.inf
    best_a, best_b = 0, 0
    for a in range(max_b):
        for b in range(max_b):
            if a * A[0] + b * B[0] == X:
                if a * A[1] + b * B[1] == Y:
                    cost = cost_A * a + cost_B * b
                    if cost < min_cost:
                        min_cost = cost
                        best_a, best_b = a, b

    return best_a, best_b, min_cost


part2()
