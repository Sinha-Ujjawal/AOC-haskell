from enum import StrEnum
from pathlib import Path
from typing import Generator


class Direction(StrEnum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    def apply(self, start: int, amount: int) -> int:
        if self == Direction.LEFT:
            return (start - amount) % 100
        elif self == Direction.RIGHT:
            return (start + amount) % 100
        else:
            raise NotImplementedError("Unreachable!")


def apply_rotations(
    start: int, rotations: list[tuple[Direction, int]]
) -> Generator[int, None, int]:
    ret = start
    yield ret
    for direction, amount in rotations:
        ret = direction.apply(start=ret, amount=amount)
        yield ret
    return ret


def main() -> None:
    file_path = input("Enter file path: ")
    rotations: list[tuple[Direction, int]] = []
    for line in Path(file_path).read_text().splitlines():
        if line.startswith("L"):
            rotations.append((Direction.LEFT, int(line[1:])))
        elif line.startswith("R"):
            rotations.append((Direction.RIGHT, int(line[1:])))

    # Part 1
    part1_ans = 0
    for posn in apply_rotations(start=50, rotations=rotations):
        if posn == 0:
            part1_ans += 1
    print(f"Part 1: {part1_ans}")

    # Part 2
    part2_ans = 0
    for posn in apply_rotations(
        start=50,
        rotations=[
            (direction, 1) for direction, amount in rotations for _ in range(amount)
        ],
    ):
        if posn == 0:
            part2_ans += 1
    print(f"Part 2: {part2_ans}")


if __name__ == "__main__":
    main()
