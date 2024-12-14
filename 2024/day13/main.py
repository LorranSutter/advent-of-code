import os
import re
import math

script_dir = os.path.dirname(__file__)
rel_path = "input_sample"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    buttons_a, buttons_b, prizes = read_file()

    tokens_spend = 0
    for i in range(len(prizes)):
        best_a, best_b, min_cost = minimize_cost(
            buttons_a[i], buttons_b[i], 3, 1, prizes[i][0], prizes[i][1]
        )
        if min_cost != math.inf:
            # print(best_a, best_b, min_cost)
            tokens_spend += min_cost

    print("Tokens spend:", tokens_spend)


def part2():
    buttons_a, buttons_b, prizes = read_file()
    shift = 10000000000000

    tokens_spend = 0
    for i in range(len(prizes)):
        print(i)
        # button_a = (buttons_a[i][0]+shift//100000000,buttons_a[i][1]+shift//100000000)
        # button_b = (buttons_b[i][0]+shift//100000000,buttons_b[i][1]+shift//100000000)
        prize = (prizes[i][0] + shift, prizes[i][1] + shift)
        # best_a, best_b, min_cost = minimize_cost(
        #     button_a, button_b, 3, 1, prize[0], prize[1]
        # )
        best_a, best_b, min_cost = minimize_cost(
            buttons_a[i], buttons_b[i], 3, 1, prize[0], prize[1]
        )
        if min_cost == 0:
            print(best_a, best_b, min_cost)
        if min_cost == math.inf:
            print(best_a, best_b, min_cost)
        if min_cost != math.inf:
            # print(best_a, best_b, min_cost)
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


def minimize_cost(A, B, cost_A, cost_B, X, Y):
    max_b = X // B[0] if X > Y else Y // B[1]
    # max_b = 100000000
    # print(max_b)
    # Check feasibility using the GCD
    # det = A[0] * B[1] - A[1] * B[0]
    gcd = math.gcd(A[0],A[1],B[0],B[1])
    # print(A,B,cost_A,cost_B,X,Y)
    # print(det,X)
    # print(det,X,math.gcd(det,X))
    # print(det,Y,math.gcd(det,Y))
    # if math.gcd(det, X) != 1 or math.gcd(det, Y) != 1:
    if X % gcd != 0 or Y % gcd != 0:
        print('here')
        # print(det,math.gcd(det, X),math.gcd(det, Y))
        return 0,0,0

    # Try all possible values of b within a reasonable range
    best_cost = math.inf
    best_a, best_b = 0, 0
    for b in range(0, max_b):
        # if b%1000000 == 0:
        #     print(max_b-b)
        # print((X - B[0] * b) % A[0])
        # input()
        if (X - B[0] * b) % A[0] == 0:
            a = (X - B[0] * b) // A[0]
            if A[1] * a + B[1] * b == Y:  # Verify the second equation
                cost = cost_A * a + cost_B * b
                if cost < best_cost:
                    best_cost = cost
                    best_a, best_b = a, b

    return best_a, best_b, best_cost


def brute_force(A, B, cost_A, cost_B, X, Y):
    max_b = X // B[0] if X > Y else Y // B[1]

    print(A, B, cost_A, cost_B, X, Y)

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
