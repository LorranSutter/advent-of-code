import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)

left, right = [], []
with open(abs_file_path) as f:
    for line in f:
        line = list(map(int, line.split()))
        left.append(line[0])
        right.append(line[1])
        
    left.sort()
    right.sort()

    s = 0
    for l, r in zip(left, right):
        s += abs(l-r)
    
    print('Total distance: ', s)