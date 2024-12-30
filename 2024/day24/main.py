import os
from typing import List
from dataclasses import dataclass


@dataclass
class Gate:
    wire1: str
    op: str
    wire2: str
    result: str


script_dir = os.path.dirname(__file__)
rel_path = "input"
abs_file_path = os.path.join(script_dir, rel_path)


def part1():
    wires, gates = read_file()
    simulate(wires, gates)
    output = get_z_output(wires)

    print("Output:", output)


def part2():
    pass


def read_file():
    wires, gates = {}, []
    with open(abs_file_path) as f:
        for line in f:
            if line == "\n":
                break

            line = line.rstrip("\n").split(": ")
            wires[line[0]] = int(line[1])

        for line in f:
            gate, result = line.rstrip("\n").split(" -> ")
            gate = gate.split()

            gates.append(Gate(gate[0], gate[1], gate[2], result))

    return wires, gates


def simulate(wires: dict, gates: List[Gate]):
    i = -1
    while len(gates) > 0:
        i += 1
        if gates[i].wire1 in wires and gates[i].wire2 in wires:
            wires[gates[i].result] = op(gates[i], wires)
            gates.pop(i)
            i = -1


def op(gate: Gate, wires: dict):
    if gate.op == "AND":
        return wires[gate.wire1] & wires[gate.wire2]
    if gate.op == "OR":
        return wires[gate.wire1] | wires[gate.wire2]
    if gate.op == "XOR":
        return wires[gate.wire1] ^ wires[gate.wire2]


def get_z_output(wires: dict) -> int:
    zeds = {wire: wires[wire] for wire in wires.keys() if wire.startswith("z")}
    output = "".join([str(item[1]) for item in sorted(zeds.items(), reverse=True)])
    return int(output, 2)


part1()
