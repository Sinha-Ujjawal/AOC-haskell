from pathlib import Path


def is_invalid(num: int) -> bool:
    num_str = str(num)
    if len(num_str) & 1:  # Odd length numbers can never be invalid
        return False
    half = len(num_str) >> 1
    return num_str[:half] == num_str[half:]


def is_invalid_v2(num: int) -> bool:
    num_str = str(num)

    def check(i: int) -> bool:
        # Checks if joining num_str[:i]  >= 2 times equals num_str
        if len(num_str) % i != 0:
            return False
        return (num_str[:i] * (len(num_str) // i)) == num_str

    for i in range(1, len(num_str)):
        if num_str[i] == num_str[0] and check(i):
            return True
    return False


def main() -> None:
    file_path = input("Enter file path: ")
    id_ranges: list[tuple[int, int]] = []
    for id_range_str in Path(file_path).read_text().split(","):
        start, end = map(int, id_range_str.split("-"))
        id_ranges.append((start, end))
    # Part 1
    part1_ans = 0
    for start, end in id_ranges:
        for num in range(start, end + 1):
            if is_invalid(num):
                part1_ans += num
    print(f"Part 1: {part1_ans}")
    # Part 2
    part2_ans = 0
    for start, end in id_ranges:
        for num in range(start, end + 1):
            if is_invalid_v2(num):
                part2_ans += num
    print(f"Part 2: {part2_ans}")


if __name__ == "__main__":
    main()
