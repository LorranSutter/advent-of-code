import os
import collections

from utils.timer import timer

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


@timer
def part1():
    rules = collections.defaultdict(lambda: [])
    updates = []
    with open(abs_file_path) as f:
        # Rules
        for line in f:
            if line == "\n":
                break
            line = line.rstrip("\n").split("|")
            if line[0] in rules:
                rules[line[0]].append(line[1])
            else:
                rules[line[0]] = [line[1]]

        s_mid_pages = 0
        for updates in f:
            pages = updates.rstrip("\n").split(",")
            if isCorrectlyOrdered(rules, pages):
                s_mid_pages += int(pages[len(pages) // 2])

    print("Sum middle pages:", s_mid_pages)


@timer
def part2():
    rules = collections.defaultdict(lambda: [])
    updates = []
    with open(abs_file_path) as f:
        # Rules
        for line in f:
            if line == "\n":
                break
            line = line.rstrip("\n").split("|")
            if line[0] in rules:
                rules[line[0]].append(line[1])
            else:
                rules[line[0]] = [line[1]]

        s_mid_pages = 0
        for updates in f:
            pages = updates.rstrip("\n").split(",")
            ordered_pages = orderIfNeeded(rules, pages.copy(), 0, len(pages))
            if pages != ordered_pages:
                s_mid_pages += int(ordered_pages[len(ordered_pages) // 2])

    print("Sum middle pages:", s_mid_pages)


def isCorrectlyOrdered(rules, pages):
    for i, first_page in enumerate(pages[:-1], 1):
        for page_after in pages[i:]:
            if page_after not in rules[first_page]:
                return False
    return True


def orderIfNeeded(rules, pages, index, size):
    if index >= size - 1:
        return pages

    for i in range(index, size - 1):
        for page_after in pages[i + 1 :]:
            if page_after not in rules[pages[i]]:
                pushToEnd(pages, i)
                return orderIfNeeded(rules, pages, i, size)

    return pages


def pushToEnd(l, index):
    item = l.pop(index)
    l.append(item)


part2()
