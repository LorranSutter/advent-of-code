import os
from collections import Counter

from utils.timer import timer

"""
Part 1:
- We need the first spot where the last n characters (n=4 here) are all different. "All different" is the same as
  saying the set of characters in that window has exactly n entries, so we never compare characters pairwise -- we
  just watch the size of a Counter over a sliding window of width n.
- We seed a Counter with the first n characters, then slide one character at a time: drop the character leaving on
  the left, add the character arriving on the right. The `counter = +counter` line is the bit of Python magic that
  makes this work -- unary plus on a Counter returns a copy with only the positive counts, so a character whose
  count just dropped to zero disappears instead of lingering with count 0 and inflating `len(counter)`.
- The distinctness check sits at the top of the loop, so it always tests the window built on the previous pass.
  That is why a match reports `i` directly: by the time iteration `i` runs, `i` characters have been processed and
  the window we are checking is the one ending just before position `i`.
- here's a run of n=4 over "mjqjpqmgbljsphdztnvjfqwrcgsmlb", which should answer 7:

    seed   window "mjqj"   counter {m:1, j:2, q:1}         len 3
    i=4    len 3 != 4   slide out 'm', in 'p'  ->  window "jqjp"   {j:2, q:1, p:1}
    i=5    len 3 != 4   slide out 'j', in 'q'  ->  window "qjpq"   {j:1, q:2, p:1}
    i=6    len 3 != 4   slide out 'q', in 'm'  ->  window "jpqm"   {j:1, q:1, p:1, m:1}
    i=7    len 4 == 4   ->  report 7

Part 2:
- Exactly the same routine, called with n=14 instead of n=4: a start-of-message marker is just a start-of-packet
  marker with a wider window.
"""


@timer
def part1():
    buffer = parse_file("input.txt")

    num_char_processed = process_datastream(buffer, 4)

    print(f"Characters processed: {num_char_processed}")


@timer
def part2():
    buffer = parse_file("input.txt")

    num_char_processed = process_datastream(buffer, 14)

    print(f"Characters processed: {num_char_processed}")


def process_datastream(buffer: str, n: int) -> int:
    num_char_processed = n
    char_processed = buffer[:n]
    counter = Counter(char_processed)

    for i in range(n, len(buffer)):
        if len(counter) == n:
            num_char_processed = i
            break

        counter[buffer[i - n]] -= 1
        counter = +counter  # Remove <= 0 counts

        counter[buffer[i]] += 1

    return num_char_processed


def parse_file(file_name: str) -> str:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, file_name)

    buffer = []
    with open(abs_file_path, "r") as f:
        buffer = f.read().strip()
    return buffer


part1()
part2()
