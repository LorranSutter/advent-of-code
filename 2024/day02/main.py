import os

from utils.timer import timer

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    safe_reports = 0
    with open(abs_file_path) as f:
        for line in f:
            levels = list(map(int, line.split()))
            if checkLevels(levels):
                safe_reports += 1

        print("Safe reports:", safe_reports)


@timer
def part2():
    safe_reports = 0
    with open(abs_file_path) as f:
        for line in f:

            safe_reports += 1
            current_sign = 0
            levels = list(map(int, line.split()))

            for i in range(len(levels) - 1):
                diff = levels[i] - levels[i + 1]
                if not checkPair(diff, current_sign):
                    # check if more damps are needed
                    if checkLevels(levels[: i - 1] + levels[i:]):
                        break
                    elif checkLevels(levels[:i] + levels[i + 1 :]):
                        break
                    elif checkLevels(levels[: i + 1] + levels[i + 2 :]):
                        break

                    # would need more damps
                    safe_reports -= 1
                    break

                current_sign = diff

        print("Safe reports:", safe_reports)


def checkPair(diff, current_sign):
    if diff == 0 or abs(diff) > 3:
        return False
    elif diff * current_sign < 0:  # 0 * 1 >= 0, 0 * -1 >= 0, 1 * 2 >= 0, -1 * -2 >= 0
        return False
    return True


def checkLevels(levels):
    current_sign = 0
    for i in range(len(levels) - 1):
        diff = levels[i] - levels[i + 1]
        if diff == 0 or abs(diff) > 3:
            return False
        elif (
            diff * current_sign < 0
        ):  # 0 * 1 >= 0, 0 * -1 >= 0, 1 * 2 >= 0, -1 * -2 >= 0
            return False
        current_sign = diff
    return True


part2()
