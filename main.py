# import copy

def find_next_empty(puzzle):
    # row, col= find_next_empty
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c
    return None, None


def is_valid(puzzle, guess, row, col):
    num_row = puzzle[row]
    if guess in num_row:
        return False
    # col_num= []
    # for i in range(9):
    # col_num.append(puzzle[i][col])
    col_num = [puzzle[i][col] for i in range(9)]
    if guess in col_num:
        return False

    row_begin = (row // 3) * 3
    col_begin = (col // 3) * 3
    for r in range(row_begin, row_begin + 3):
        for c in range(col_begin, col_begin + 3):
            if puzzle[r][c] == guess:
                return False
    return True


def solve_sudoku(puzzle):
    # make puzzle2 a deep copy of puzzle
    # puzzle2 = deepcopy.puzzle
    row, col = find_next_empty(puzzle)
    if row is None:
        return True
    for guess in range(1, 10):
        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess
            if solve_sudoku(puzzle):
                return True

            puzzle[row][col] = -1
        return False

    # list in list is a row in the sudoku board


if __name__ == '__main__':
    sudoku_board = [
        [3, 9, -1, -1, 5, -1, -1, -1, -1],
        [-1, -1, -1, 2, -1, -1, -1, -1, 5],
        [-1, -1, -1, 7, 1, 9, -1, 8, -1],

        [-1, 5, -1, -1, 6, 8, -1, -1, -1],
        [2, -1, 6, -1, -1, 3, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, 4],

        [5, -1, -1, -1, -1, -1, -1, -1, -1],
        [6, 7, -1, 1, -1, 5, -1, 4, -1],
        [1, -1, 9, -1, -1, -1, 2, -1, -1]
    ]

    print(solve_sudoku(sudoku_board))
    print(sudoku_board)
