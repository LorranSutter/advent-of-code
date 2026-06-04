#!/usr/bin/env python3
"""
Scans all day folders and generates progress summaries:
- Root README.md: overall stats + progress bars per year
- year/README.md: detailed day tables with stars

For each day's main.py, it checks whether part1(), part2() contain
a "# TODO" comment in the first non-empty line of the function body. If so,
the part is considered unsolved.

The root summary is injected between <!-- SUMMARY:START --> and <!-- SUMMARY:END -->
markers in README.md, preserving all other content.

Each year/README.md is managed between <!-- SUMMARY:START --> and
<!-- SUMMARY:END --> markers as well, so any content outside the markers
(like the title) is preserved after the first run.
"""

import re
from pathlib import Path


ROOT = Path(__file__).parent


def find_days(root: Path) -> dict:
    """
    Returns a nested dict: {year: {day_number: {part: solved}}}
    """
    results = {}

    for year_dir in sorted(root.iterdir()):
        if not year_dir.is_dir() or not year_dir.name.isdigit():
            continue
        year = year_dir.name

        for day_dir in sorted(year_dir.iterdir()):
            if not day_dir.is_dir():
                continue
            match = re.match(r"day(\d+)", day_dir.name)
            if not match:
                continue

            day_num = int(match.group(1))
            main_file = day_dir / "main.py"
            if not main_file.exists():
                continue

            parts = check_parts(main_file)
            results.setdefault(year, {})[day_num] = parts

    return results


def check_parts(main_file: Path) -> dict:
    """
    Parses main.py and checks if part1/part2 functions have a # TODO
    in the first non-empty line of the function body.
    Returns {1: True/False, 2: True/False} where True = solved.
    """
    content = main_file.read_text()
    parts = {}

    for part_num in [1, 2]:
        pattern = rf"def part{part_num}\(.*?\):\s*\n(.*?)(?=\ndef |\Z)"
        match = re.search(pattern, content, re.DOTALL)

        if not match:
            parts[part_num] = False
            continue

        body = match.group(1)
        first_code_line = ""
        for line in body.split("\n"):
            stripped = line.strip()
            if stripped:
                first_code_line = stripped
                break

        parts[part_num] = "# TODO" not in first_code_line

    return parts


def get_total_days(year: str) -> int:
    """Returns the expected total number of days for the given year."""
    if year == "2025":
        return 12
    return 25


def generate_root_summary(results: dict) -> str:
    """Generates the root README summary with progress bars per year."""
    lines = []
    lines.append("## 📊 Progress")
    lines.append("")

    total_solved = 0
    total_parts = 0

    section_lines = []

    for year in sorted(results.keys()):
        days = results[year]

        solved = sum(
            1 for d in days.values() for p, s in d.items() if s
        )
        total_days = get_total_days(year)
        total = total_days * 2
        total_solved += solved
        total_parts += total

        pct = (solved / total * 100) if total > 0 else 0
        filled = round(pct / 5)
        bar = "█" * filled + "░" * (20 - filled)

        section_lines.append(f"### [{year}](./{year}/)")
        section_lines.append("")
        section_lines.append(f"`{bar}` **{solved}/{total}** parts solved ({pct:.0f}%)")
        section_lines.append("")

    # Overall summary
    overall_pct = (total_solved / total_parts * 100) if total_parts > 0 else 0
    lines.append(f"> **Overall: {total_solved}/{total_parts} parts solved ({overall_pct:.0f}%)**")
    lines.append("")
    lines.extend(section_lines)

    return "\n".join(lines)


def generate_year_readme(year: str, days: dict) -> str:
    """Generates the day table for a year README."""
    total_days = get_total_days(year)
    solved = sum(1 for d in days.values() for p, s in d.items() if s)
    total = total_days * 2
    pct = (solved / total * 100) if total > 0 else 0
    filled = round(pct / 5)
    bar = "█" * filled + "░" * (20 - filled)

    lines = []
    lines.append(f"`{bar}` **{solved}/{total}** parts solved ({pct:.0f}%)")
    lines.append("")
    lines.append("| Day | Part 1 | Part 2 |")
    lines.append("|:----|:------:|:------:|")

    max_day = max([total_days] + list(days.keys()))
    for day_num in range(1, max_day + 1):
        if day_num in days:
            parts = days[day_num]
            cols = []
            for p in [1, 2]:
                cols.append("⭐" if parts.get(p, False) else "⬚")
            lines.append(
                f"| [Day {day_num:02d}](./day{day_num:02d}/) | {cols[0]} | {cols[1]} |"
            )
        else:
            lines.append(
                f"| Day {day_num:02d} | ⬚ | ⬚ |"
            )

    lines.append("")
    return "\n".join(lines)



def inject_between_markers(content: str, summary: str, default_header: str) -> str:
    """
    Replaces content between <!-- SUMMARY:START --> and <!-- SUMMARY:END --> markers.
    If markers don't exist, creates the file with a header + markers.
    """
    start_marker = "<!-- SUMMARY:START -->"
    end_marker = "<!-- SUMMARY:END -->"
    block = f"{start_marker}\n{summary}\n{end_marker}"

    if start_marker in content and end_marker in content:
        pattern = re.compile(
            re.escape(start_marker) + r".*?" + re.escape(end_marker),
            re.DOTALL,
        )
        return pattern.sub(block, content)
    else:
        # No markers yet — create with default header
        return f"{default_header}\n\n{block}\n"


def update_root_readme(root: Path, summary: str) -> None:
    """Injects the summary into the root README.md between markers."""
    readme_path = root / "README.md"
    content = readme_path.read_text()

    start_marker = "<!-- SUMMARY:START -->"
    end_marker = "<!-- SUMMARY:END -->"
    block = f"{start_marker}\n{summary}\n{end_marker}"

    if start_marker in content and end_marker in content:
        pattern = re.compile(
            re.escape(start_marker) + r".*?" + re.escape(end_marker),
            re.DOTALL,
        )
        new_content = pattern.sub(block, content)
    else:
        # Insert after the intro paragraph
        intro_pattern = re.compile(
            r"(# .+\n\n.+\n\n.+\n)"
        )
        match = intro_pattern.match(content)
        if match:
            insert_pos = match.end()
            new_content = (
                content[:insert_pos] + "\n" + block + "\n\n" + content[insert_pos:]
            )
        else:
            new_content = content + "\n\n" + block + "\n"

    readme_path.write_text(new_content)
    print(f"✅ Updated {readme_path}")


def update_year_readme(root: Path, year: str, table_summary: str) -> None:
    """Creates or updates the year/README.md with the day table."""
    readme_path = root / year / "README.md"
    default_header = f"# {year}"

    if readme_path.exists():
        content = readme_path.read_text()
    else:
        content = ""

    new_content = inject_between_markers(content, table_summary, default_header)
    readme_path.write_text(new_content)
    print(f"✅ Updated {readme_path}")


def main():
    results = find_days(ROOT)

    # Generate and update root README
    root_summary = generate_root_summary(results)
    update_root_readme(ROOT, root_summary)

    # Generate and update each year README
    for year in sorted(results.keys()):
        days = results[year]
        table_summary = generate_year_readme(year, days)
        update_year_readme(ROOT, year, table_summary)


if __name__ == "__main__":
    main()
