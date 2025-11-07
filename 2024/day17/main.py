import os

script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    A, B, C, program = read_file()

    size = len(program)
    pointer = 0
    output = []
    while True:
        if pointer + 1 >= size:
            break

        op = program[pointer]
        operand = program[pointer + 1]
        A, B, C, pointer, out = ops[op](A, B, C, operand, pointer)

        if out != None:
            output.append(str(out))

    print("Output:", ",".join(output))


def part2():
    A, B_initial, C_initial, program = read_file()

    A_initial, B, C = 567314000, B_initial, C_initial
    size = len(program)
    pointer = 0
    output = []
    biggest_output = []
    while True:
        if pointer + 1 >= size:
            break

        op = program[pointer]
        operand = program[pointer + 1]
        A, B, C, pointer, out = ops[op](A, B, C, operand, pointer)

        if out != None:
            output.append(str(out))
            if len(output) > len(biggest_output):
                biggest_output = output
        if A_initial % 1000 == 0:
            print(A_initial,output,biggest_output)
        if output == program:
            break
        else:
            for i in range(len(output)):
                if output[i] != program[i]:
                    A_initial += 8
                    A  = A_initial
                    B, C = B_initial, C_initial
                    pointer = 0
                    output = []

    print("A:", A)


def read_file():
    with open(abs_file_path) as f:
        A = int(f.readline().rstrip("\n").split(":")[1])
        B = int(f.readline().rstrip("\n").split(":")[1])
        C = int(f.readline().rstrip("\n").split(":")[1])
        f.readline()
        program = list(map(int, f.readline().rstrip("\n").split(":")[1].split(",")))
    return A, B, C, program


def combo_operand(A, B, C, operand):
    if operand == 4:
        return A
    if operand == 5:
        return B
    if operand == 6:
        return C
    return operand


def op0(A, B, C, operand, pointer):
    A //= 2 ** combo_operand(A, B, C, operand)
    return A, B, C, pointer + 2, None


def op1(A, B, C, operand, pointer):
    B ^= operand
    return A, B, C, pointer + 2, None


def op2(A, B, C, operand, pointer):
    B = combo_operand(A, B, C, operand) % 8
    return A, B, C, pointer + 2, None


def op3(A, B, C, operand, pointer):
    if A == 0:
        return A, B, C, pointer + 2, None
    return A, B, C, operand, None


def op4(A, B, C, _, pointer):
    B ^= C
    return A, B, C, pointer + 2, None


def op5(A, B, C, operand, pointer):
    return A, B, C, pointer + 2, combo_operand(A, B, C, operand) % 8


def op6(A, B, C, operand, pointer):
    B = A // (2 ** combo_operand(A, B, C, operand))
    return A, B, C, pointer + 2, None


def op7(A, B, C, operand, pointer):
    C = A // (2 ** combo_operand(A, B, C, operand))
    return A, B, C, pointer + 2, None


ops = [op0, op1, op2, op3, op4, op5, op6, op7]

part2()
