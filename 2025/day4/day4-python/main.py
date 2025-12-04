from dataclasses import dataclass
from pathlib import Path
from typing import NewType

Position = NewType("Position", tuple[int, int])


def neighbors(pos: Position) -> list[Position]:
    ret = []
    for offx in [-1, 0, 1]:
        for offy in [-1, 0, 1]:
            if offx == 0 and offy == 0:
                continue
            ret.append((pos[0] + offx, pos[1] + offy))
    return ret


@dataclass(slots=True)
class Grid:
    matrix: list[list[str]]
    width: int
    height: int

    def __init__(self, matrix: list[list[str]]):
        self.matrix = matrix
        self.width = len(matrix[0])
        self.height = len(matrix)

    def at(self, pos: Position) -> str:
        x, y = pos
        return self.matrix[y][x]

    def set_at(self, pos: Position, new: str):
        x, y = pos
        self.matrix[y][x] = new

    def count_rolls_in_neighbors(self, pos: Position) -> int:
        count_of_rolls = 0
        for npos in neighbors(pos):
            if (
                0 <= npos[0] < self.width
                and 0 <= npos[1] < self.height
                and self.at(npos) == "@"
            ):
                count_of_rolls += 1
        return count_of_rolls

    def grazable_positions(self) -> list[Position]:
        ret = []
        for x in range(self.width):
            for y in range(self.height):
                pos = Position((x, y))
                if self.at(pos) == "@":
                    count_of_rolls = self.count_rolls_in_neighbors(pos)
                    if count_of_rolls < 4:
                        ret.append(pos)
        return ret

    def graze_positions(self, positions: list[Position]):
        for pos in positions:
            self.set_at(pos, ".")


def solve1(grid: Grid) -> int:
    return len(grid.grazable_positions())


def solve2(grid: Grid) -> int:
    ret = 0
    while True:
        grazable_positions = grid.grazable_positions()
        if not grazable_positions:
            break
        ret += len(grazable_positions)
        grid.graze_positions(grazable_positions)
    return ret


def main() -> None:
    file_path = input("Enter file path: ")
    grid = Grid(list(map(list, Path(file_path).read_text().splitlines())))
    # Part 1
    part1_ans = solve1(grid)
    print(f"Part 1: {part1_ans}")
    # Part 2
    part2_ans = solve2(grid)
    print(f"Part 2: {part2_ans}")


if __name__ == "__main__":
    main()
