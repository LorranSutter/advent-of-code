import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    rules = {}
    updates = []
    with open(abs_file_path) as f:
        # Rules
        for line in f:
            if line == '\n':
                break
            line = line.rstrip('\n').split('|')
            if line[0] in rules:
                rules[line[0]].append(line[1])
            else:
                rules[line[0]] = [line[1]]
        
        s_mid_pages = 0
        for updates in f:
            pages = updates.rstrip('\n').split(',')
            if isCorrectlyOrdered(rules, pages):
                s_mid_pages += int(pages[len(pages)//2])
            print()

    print("Sum middle pages:", s_mid_pages)


def part2():
    pass


def isCorrectlyOrdered(rules, pages):
    for i, first_page in enumerate(pages[:-1],1):
        if first_page not in rules:
            return False
        for page_after in pages[i:]:
            if page_after not in rules[first_page]:
                return False
    return True

part1()
