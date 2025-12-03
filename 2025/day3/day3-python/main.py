from functools import partial
from pathlib import Path


def largest_k_subsequence(digits, k):
    stack = []
    to_remove = len(digits) - k

    for d in digits:
        while stack and to_remove > 0 and stack[-1] < d:
            stack.pop()
            to_remove -= 1
        stack.append(d)

    return int("".join(map(str, stack[:k])))


def largest_possible_joltage(digits_array: list[list[int]], size: int = 2) -> int:
    return sum(map(partial(largest_k_subsequence, k=size), digits_array))


def main() -> None:
    file_path = input("Enter file path: ")
    digits_array = [
        list(map(int, line)) for line in Path(file_path).read_text().splitlines()
    ]
    # Part 1
    part1_ans = largest_possible_joltage(digits_array)
    print(f"Part 1: {part1_ans}")
    # Part 2
    part2_ans = largest_possible_joltage(digits_array, 12)
    print(f"Part 2: {part2_ans}")


if __name__ == "__main__":
    main()
