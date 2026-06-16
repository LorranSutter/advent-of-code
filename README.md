# 🎄 Advent of Code

[![Dashboard](https://img.shields.io/badge/Dashboard-coding--challenges-blue?style=for-the-badge)](https://github.com/LorranSutter/coding-challenges) <!-- BADGE:START -->[![Solved Challenges](https://img.shields.io/badge/Solved%20Challenges-100-brightgreen?style=for-the-badge&logo=python&logoColor=white)](https://adventofcode.com/)<!-- BADGE:END -->

This repository contains my solutions for the [Advent of Code](https://adventofcode.com/) event.

Advent of Code is an annual coding challenge that runs from December 1st to December 25th, featuring daily programming puzzles of varying difficulty.

<!-- SUMMARY:START -->
## 📊 Progress

> **Overall: 100/124 parts solved (81%)**

### [2023](./2023/)

`██████████████░░░░░░` **34/50** parts solved (68%)

### [2024](./2024/)

`██████████████████░░` **45/50** parts solved (90%)

### [2025](./2025/)

`██████████████████░░` **21/24** parts solved (88%)

<!-- SUMMARY:END -->

## 🛠️ Setup

### Creating a Virtual Environment

```bash
python3 -m venv .venv
```

### Activating the Virtual Environment

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### Installing Dependencies

```bash
pip install -r requirements.txt
```

Deactivating the Virtual Environment

```bash
deactivate
```

## ✨ Creating a New Puzzle

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

## 🚀 Running Solutions

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

## 🔄 Updating Progress Summary

To update the progress summary in this README after solving new parts, run the `generate_readme.py` script:

```bash
python3 generate_readme.py
```