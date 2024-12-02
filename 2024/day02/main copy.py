import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)

def part1():
    safe_reports = 0
    with open(abs_file_path) as f:
        for line in f:

            safe_reports += 1
            current_sign = 0
            levels = list(map(int, line.split()))

            for i in range(len(levels)-1):
                diff = levels[i] - levels[i+1]
                if abs(diff) == 0 or abs(diff) > 3:
                    safe_reports -= 1
                    break
                elif diff * current_sign < 0: # 0 * 1 >= 0, 0 * -1 >= 0, 1 * 2 >= 0, -1 * -2 >= 0
                    safe_reports -= 1
                    break
                current_sign = diff

        print('Safe reports:', safe_reports)

def checkLevels(diff, current_sign):
    if abs(diff) == 0 or abs(diff) > 3:
        return False
    elif diff * current_sign < 0: # 0 * 1 >= 0, 0 * -1 >= 0, 1 * 2 >= 0, -1 * -2 >= 0
        return False
    return True

def part2():
    safe_reports = 0
    with open(abs_file_path) as f:
        for line in f:

            safe_reports += 1
            current_sign = 0
            damped = False
            levels = list(map(int, line.split()))

            for i in range(len(levels)-1):
                diff = levels[i] - levels[i+1]
                if not checkLevels(diff, current_sign):
                    dumped = True
                    if checkLevels(levels, i, i+1, current_sign):
                diff = levels[i] - levels[i+1]
                if abs(diff) == 0 or abs(diff) > 3:
                    safe_reports -= 1
                    break
                elif diff * current_sign < 0: # 0 * 1 >= 0, 0 * -1 >= 0, 1 * 2 >= 0, -1 * -2 >= 0
                    safe_reports -= 1
                    break
                current_sign = diff

        print('Safe reports:', safe_reports)
            