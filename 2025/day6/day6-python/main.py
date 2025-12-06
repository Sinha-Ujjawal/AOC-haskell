from pathlib import Path


def parse_input(input_str: str) -> list[tuple[str, list[str]]]:
    lines = input_str.splitlines()
    max_len = max(map(len, lines))
    lines = list(map(lambda line: line.ljust(max_len), lines))
    symbols = lines[-1].split()
    matrices = []
    acc = [""] * (len(lines) - 1)
    for col in range(len(lines[0])):
        all_space = True
        for row in range(len(lines) - 1):
            if lines[row][col] != " ":
                all_space = False
            acc[row] += lines[row][col]
        if all_space:
            matrix = []
            for i in range(len(acc)):
                matrix.append(acc[i][:-1])
                acc[i] = ""
            matrices.append(matrix)

    matrix = []
    for i in range(len(acc)):
        matrix.append(acc[i])
        acc[i] = ""
    matrices.append(matrix)
    return list(zip(symbols, matrices))


def transpose_str(rows: list[str]) -> list[str]:
    max_len = max(map(len, rows))
    matrix = list(map(lambda row: row.rjust(max_len), rows))
    nrows, ncols = len(matrix), max_len
    return ["".join(matrix[row][col] for row in range(nrows)) for col in range(ncols)]


def main() -> None:
    file_path = input("Enter file path: ")
    input_str = Path(file_path).read_text()
    symbols_and_matrices = parse_input(input_str)
    # Part 1
    part1_ans = sum(
        eval(symbol.join(matrix)) for symbol, matrix in symbols_and_matrices
    )
    print(f"Part 1: {part1_ans}")
    # Part 2
    part2_ans = sum(
        eval(symbol.join(transpose_str(matrix)))
        for symbol, matrix in symbols_and_matrices
    )
    print(f"Part 2: {part2_ans}")


if __name__ == "__main__":
    main()
