# created by Sijmen van der Willik
# 09/03/2018 19:59

import numpy as np

grid_size = 6

base_grid = np.zeros(shape=(grid_size, grid_size), dtype=int)

# orders are: top right bottom left
#             0   1     2      3
# indices are left to right, top to bottom

base_constraints = [
    [0, 0, 2],
    [0, 1, 2],
    [0, 2, 1],
    [0, 3, 3],
    [0, 4, 5],
    [0, 5, 4],
    [1, 0, 4],
    [1, 1, 4],
    [1, 2, 3],
    [1, 3, 1],
    [1, 4, 2],
    [1, 5, 2],
    [2, 0, 3],
    [2, 1, 2],
    [2, 2, 5],
    [2, 3, 2],
    [2, 4, 1],
    [2, 5, 2],
    [3, 0, 3],
    [3, 1, 1],
    [3, 2, 3],
    [3, 3, 4],
    [3, 4, 2],
    [3, 5, 4]
]


def get_count(numbers):
    result = 0
    max_n = 0

    for number in numbers:
        if number > max_n:
            result += 1
            max_n = number

    return result


def violates(grid, constraint):
    if constraint[0] == 0:
        numbers = grid[:, constraint[1]]
    elif constraint[0] == 1:
        numbers = grid[constraint[1], :][::-1]
    elif constraint[0] == 2:
        numbers = grid[:, constraint[1]][::-1]
    elif constraint[0] == 3:
        numbers = grid[constraint[1], :]
    else:
        print("LOL shouldn't be here wtf")
        numbers = "fail"

    if 0 in numbers:
        return False

    target = constraint[2]

    count = get_count(numbers)

    return target != count


def fits(i, grid, row, col, constraints):
    # check if in row
    if i in grid[row, :]:
        return False
    
    # check if in column
    if i in grid[:, col]:
        return False

    # check constraints
    for constraint in constraints:
        old = grid[row, col]

        grid[row, col] = i

        if violates(grid, constraint):
            return False

        grid[row, col] = old

    return True


def solve(grid, n, constraints):

    if n <= 3:
        print(grid[0])

    if n == grid_size ** 2:
        print("\n===================================================")
        print("======================RESULT=======================")
        print("===================================================\n")
        print(grid)
        return True

    row = n // grid_size
    col = n % grid_size

    for i in range(1, grid_size + 1):
        if fits(i, grid, row, col, constraints):
            grid[row, col] = i
            result = solve(grid, n + 1, constraints)

            if result:
                return result

    # reset self
    grid[row, col] = 0


solve(base_grid, 0, base_constraints)
