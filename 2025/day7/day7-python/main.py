from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import NewType, Optional


class Symbol(Enum):
    DOT = "."
    START = "S"
    FORK = "^"

    @staticmethod
    def from_str(sym: str) -> "Symbol":
        if sym == ".":
            return Symbol.DOT
        elif sym == "S":
            return Symbol.START
        elif sym == "^":
            return Symbol.FORK
        else:
            raise ValueError(f"Unknown symbol: {sym}")


Position = NewType("Position", tuple[int, int])


@dataclass
class Grid:
    matrix: list[list[Symbol]]
    width: int
    height: int
    start_sym_posn: Optional[Position] = None

    def neighbors(self, posn: Position) -> list[Position]:
        y, x = posn
        if y + 1 >= self.height:
            return []
        if self.matrix[y + 1][x] == Symbol.FORK:
            return [Position((y + 1, x - 1)), Position((y + 1, x + 1))]
        return [Position((y + 1, x))]

    def count_splits(self) -> int:
        if self.start_sym_posn is None:
            return 0
        frontier = {self.start_sym_posn}
        seen_before = set()
        count = 0
        while frontier:
            new_frontier = set()
            for node in frontier:
                seen_before.add(node)
                num_neighbors = 0
                for neighbor in self.neighbors(node):
                    if neighbor in seen_before:
                        continue
                    num_neighbors += 1
                    new_frontier.add(neighbor)
                if num_neighbors > 1:
                    count += 1
            frontier = new_frontier
        return count

    def count_possible_timelines(self) -> int:
        if self.start_sym_posn is None:
            return 0
        _memo = {}

        def _dp(node: Position) -> int:
            y, x = node
            if y + 1 >= self.height:
                return 1
            if node in _memo:
                return _memo[node]
            s = 0
            for neighbor in self.neighbors(node):
                s += _dp(neighbor)
            _memo[node] = s
            return s

        return _dp(self.start_sym_posn)


def parse_input(input_str: str) -> Grid:
    lines = input_str.splitlines()
    height = len(lines)
    start_sym_posn = width = None
    matrix = []
    for row_idx, line in enumerate(lines):
        if width is None:
            width = len(line)
        else:
            width = max(width, len(line))
        row = []
        for col_idx, sym_chr in enumerate(line):
            sym = Symbol.from_str(sym_chr)
            if sym == Symbol.START:
                assert start_sym_posn is None
                start_sym_posn = Position((row_idx, col_idx))
            row.append(sym)
        matrix.append(row)
    assert width is not None
    return Grid(
        matrix=matrix,
        width=width,
        height=height,
        start_sym_posn=start_sym_posn,
    )


def main() -> None:
    file_path = input("Enter file path: ")
    input_str = Path(file_path).read_text()
    grid = parse_input(input_str)
    # print("\n".join("".join([x.value for x in row]) for row in grid))
    # Part 1
    part1_ans = grid.count_splits()
    print(f"Part 1: {part1_ans}")
    # Part 2
    part2_ans = grid.count_possible_timelines()
    print(f"Part 2: {part2_ans}")


if __name__ == "__main__":
    main()
