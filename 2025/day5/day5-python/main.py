from itertools import islice
from pathlib import Path
from typing import Iterator


def parse_input(input_str: str) -> tuple[list[tuple[int, int]], list[int]]:
    is_gathering_fresh_ingrediant_ranges: bool = True
    fresh_ingrediant_ranges: list[tuple[int, int]] = []
    ingrediants: list[int] = []
    for line in input_str.splitlines():
        line = line.strip()
        if line == "":
            is_gathering_fresh_ingrediant_ranges = False
            continue
        if is_gathering_fresh_ingrediant_ranges:
            low, high = map(int, line.split("-"))
            fresh_ingrediant_ranges.append((low, high))
        else:
            ingrediants.append(int(line))
    return fresh_ingrediant_ranges, ingrediants


def overlap(range1: tuple[int, int], range2: tuple[int, int]) -> bool:
    l1, h1 = range1
    l2, h2 = range2
    return l1 <= h2 and l2 <= h1


def non_overlapping_ranges(ranges: list[tuple[int, int]]) -> Iterator[tuple[int, int]]:
    if not ranges:
        return None
    sorted_ranges = sorted(ranges, key=lambda pair: pair[0])
    clow, chigh = sorted_ranges[0]
    for low, high in islice(sorted_ranges, 1, len(sorted_ranges)):
        if overlap((low, high), (clow, chigh)):
            clow = min(clow, low)
            chigh = max(chigh, high)
        else:
            yield clow, chigh
            clow, chigh = low, high
    yield clow, chigh


def count_fresh(
    fresh_ingrediant_ranges: list[tuple[int, int]], ingrediants: list[int]
) -> int:
    cnt = 0
    for ingrediant in ingrediants:
        if any(low <= ingrediant <= high for low, high in fresh_ingrediant_ranges):
            cnt += 1
    return cnt


def count_all_fresh(fresh_ingrediant_ranges: list[tuple[int, int]]):
    return sum(
        (high - low + 1)
        for low, high in non_overlapping_ranges(fresh_ingrediant_ranges)
    )


def main() -> None:
    file_path = input("Enter file path: ")
    fresh_ingrediant_ranges, ingrediants = parse_input(Path(file_path).read_text())
    # Part 1
    part1_ans = count_fresh(fresh_ingrediant_ranges, ingrediants)
    print(f"Part 1: {part1_ans}")
    # Part 2
    part2_ans = count_all_fresh(fresh_ingrediant_ranges)
    print(f"Part 2: {part2_ans}")


if __name__ == "__main__":
    main()
