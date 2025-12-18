# 🎄 Advent of Code

This repository contains my solutions for the [Advent of Code](https://adventofcode.com/) event.

Advent of Code is an annual coding challenge that runs from December 1st to December 25th, featuring daily programming puzzles of varying difficulty.

## Creating a New Puzzle

To create a new puzzle structure, use the `new_puzzle.sh` script:

```bash
./new_puzzle.sh <year> <day>
```

Example:
```bash
./new_puzzle.sh 2025 1
```

This will create:
- A folder structure: `2025/day01/`
- `main.py` with a template for part 1 and part 2
- `input.txt` for the puzzle input
- `input_sample.txt` for sample/test input

## Running Solutions

You can run the solutions in two ways:

### As a Python Module

```bash
python3 -m 2025.day01.main
```

### As a Script
```bash
python3 ./2025/day01/main.py
```

Replace `2025` with the desired year and `day01` with the specific day you want to run.