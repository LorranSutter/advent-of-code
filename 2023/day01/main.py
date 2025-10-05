import os

script_dir = os.path.dirname(__file__)
rel_path = "input.txt"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    calibrations = read_file()
    nums = set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])

    total = 0
    for calibration in calibrations:
        value = "0"

        # Search first digit
        for i in range(len(calibration)):
            if calibration[i] in nums:
                value += calibration[i]
                break

        # Search second digit
        for i in range(len(calibration) - 1, -1, -1):
            if calibration[i] in nums:
                value += calibration[i]
                break

        # Combine digits
        total += int(value)

    print("Total calibration value:", total)


def part2():
    calibrations = read_file()
    nums = set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    numsTextTowards = dict(
        {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }
    )
    numsTextBackwards = dict(
        {
            "eno": "1",
            "owt": "2",
            "eerht": "3",
            "ruof": "4",
            "evif": "5",
            "xis": "6",
            "neves": "7",
            "thgie": "8",
            "enin": "9",
        }
    )

    numsTextPartialTowards = set()
    numsTextPartialBackwards = set()
    for numText in numsTextTowards.keys():
        for i in range(len(numText)):
            numsTextPartialTowards.add(numText[:i])
            numsTextPartialBackwards.add(numText[len(numText)-1:i:-1])

    total = 0
    for calibration in calibrations:
        value = "0"

        # Search first digit
        word = ""
        for i in range(len(calibration)):
            # Check nums 1,2,3...
            if calibration[i] in nums:
                value = calibration[i]
                break

            # Check words one, two...
            word += calibration[i]
            if word in numsTextTowards.keys():
                value = numsTextTowards[word]
                break
            # Check partial words on, tw...
            if word not in numsTextPartialTowards:
                while len(word) > 0:
                    word = word[1:]
                    if word in numsTextPartialTowards:
                        break

        # Search second digit
        word = ""
        for i in range(len(calibration) - 1, -1, -1):
            # Check nums 1,2,3...
            if calibration[i] in nums:
                value += calibration[i]
                break

            word += calibration[i]
            # Check words one, two...
            if word in numsTextBackwards.keys():
                value += numsTextBackwards[word]
                break
            # Check partial words on, tw...
            if word not in numsTextPartialBackwards:
                while len(word) > 0:
                    word = word[1:]
                    if word in numsTextPartialBackwards:
                        break

        # Combine digits
        total += int(value)

    print("Total calibration value:", total)


def read_file():
    calibrations = []
    with open(abs_file_path) as f:
        calibrations = [line.rstrip("\n") for line in f]

    return calibrations


part2()
