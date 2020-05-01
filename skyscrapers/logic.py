# created by Sijmen van der Willik
# 13/07/2018 16:43
#
# solves the skyscraper puzzle by reducing a set of possible numbers for each cell


def set_number(row, col, n):
    # remove from col
    for tmp_row in range(grid_size):
        if type(sets[tmp_row][col]) == list and n in sets[tmp_row][col]:
            sets[tmp_row][col].remove(n)

    # remove from row
    for tmp_col in range(grid_size):
        if type(sets[row][tmp_col]) == list and n in sets[row][tmp_col]:
            sets[row][tmp_col].remove(n)

    sets[row][col] = [n]


def is_valid(l, row):

    see_n = 0
    max_h = 0

    for i in row:
        if i > max_h:
            see_n += 1
            max_h = i

    return l == see_n


def increment_counter(counters, max_counters):
    counters[-1] += 1

    for i in range(grid_size - 1, -1, -1):
        if counters[i] >= max_counters[i]:
            counters[i] = 0
            counters[i - 1] += 1
        else:
            break

    return counters


def set_permutations(row_sets):
    counters = [0 for _ in range(grid_size)]
    max_counters = [len(row_sets[i]) for i in range(grid_size)]

    loop_n = 1

    for tmp in max_counters:
        loop_n *= tmp

    # the iterator loop
    for i in range(loop_n):

        # build permutation
        col = 0
        perm = []
        for counter in counters:
            perm.append(row_sets[col][counter])
            col += 1

        yield perm

        increment_counter(counters, max_counters)


def reduce_by_constraint(l_c, r_c, row_sets):
    """Checks all possible formations of the set against the given left and right constraint

    if a number is not present in any valid solution for any given cell,
      it will be removed from the set for that cell

    :param l_c:
    :param r_c:
    :param row_sets:
    :return:
    """
    result_sets = [set() for _ in range(grid_size)]

    for permutation in set_permutations(row_sets):
        # check for duplicates, skip if contains duplicates
        if len(set(permutation)) != len(permutation):
            continue

        valid = True

        if l_c != 0:
            valid = is_valid(l_c, permutation)

        # check right constraint, flip permutation to check
        if valid and r_c != 0:
            valid = is_valid(r_c, permutation[::-1])

        if valid:
            for i in range(grid_size):
                result_sets[i].add(permutation[i])

    return [list(i) for i in result_sets]


def reduce_by_only_left(row_sets):
    """If a number is only present in one set, place the number in that cell

    i.e.
    [1, 2, 5], [1, 2], [1, 2, 3] -> [5], [1, 2], [3]

    :param row_sets:
    :return:
    """

    # for each number
    for i in range(grid_size):
        n = i + 1

        cell = -1

        # for each cell in row
        for col in range(grid_size):

            if n in row_sets[col]:
                if cell == -1:
                    cell = col
                else:
                    cell = -1
                    break

        # if only 1 cell found
        if cell != -1:
            row_sets[cell] = [n]

    return row_sets


def print_sets(p_sets):
    global n_left

    tmp_n = n_left

    n_left, n_perm = count_n_grid()

    if n_left < tmp_n:
        print("n left: {}, possible permutations: {} ({:.2E})".format(n_left, n_perm, n_perm))

        for row in p_sets:
            p_str = ""

            for col in row:
                p_str += "{:>23}".format(str(col))

            print(p_str)

        print("")


def get_col(col_n):
    result_col = []

    for i in range(grid_size):
        result_col.append(sets[i][col_n])

    return result_col


def set_col(col_n, col):
    for row_n in range(grid_size):
        sets[row_n][col_n] = col[row_n]


def solve():
    last_round = n_left + 1
    loop_counter = 0

    print("Set reduction...")
    while n_left < last_round:
        last_round = n_left
        loop_counter += 1

        print("Loop: {}".format(loop_counter))

        # constraints
        for i in range(grid_size):
            sets[i] = reduce_by_constraint(int(constraints['l'][i]),
                                           int(constraints['r'][i]),
                                           sets[i])
            print_sets(sets)

        for i in range(grid_size):
            col = get_col(i)
            new_col = reduce_by_constraint(int(constraints['t'][i]),
                                           int(constraints['b'][i]),
                                           col)
            set_col(i, new_col)
            print_sets(sets)

        # only left
        for i in range(grid_size):
            sets[i] = reduce_by_only_left(sets[i])
            print_sets(sets)

        for i in range(grid_size):
            col = get_col(i)
            new_col = reduce_by_only_left(col)
            set_col(i, new_col)
            print_sets(sets)

    print("Brute forcing...")  # TODO


def count_n_grid():
    total = 0
    total_perm = 1
    for i in range(grid_size):
        for j in range(grid_size):
            total += len(sets[i][j])
            total_perm *= len(sets[i][j])

    return total, total_perm


def load_level(n):
    """

    :param n: level number
    :return: <dict of strings> c (constraints), <int> g (grid_size), <list of lists> p (preset values)
    """
    c = {}
    g = -1
    p = []

    if n == 14:
        # top down, left to right
        c = {
            't': '10230',
            'r': '20300',
            'b': '01022',
            'l': '02330'
        }
        g = 5
    elif n == 15:
        c = {
            't': '31202',
            'r': '03200',
            'b': '20400',
            'l': '22414'
        }
        g = 5
    elif n == 29:
        c = {
            't': '0200050',
            'r': '4000303',
            'b': '3440204',
            'l': '2300340'
        }
        g = 7
        p = [
            [0, 1, 4],
            [4, 3, 3],
            [6, 2, 2]
        ]
    elif n == 30:
        c = {
            't': '0200300',
            'r': '3004223',
            'b': '2432000',
            'l': '2032002'
        }
        g = 7
        p = [
            [0, 1, 5],
            [1, 2, 2],
            [2, 2, 3],
            [4, 5, 3]
        ]

    return c, g, p


if __name__ == "__main__":
    constraints, grid_size, presets = load_level(30)
    n_left = grid_size ** 3

    sets = [[[(i + 1) for i in range(grid_size)] for _ in range(grid_size)] for _ in range(grid_size)]

    for preset in presets:
        set_number(preset[0], preset[1], preset[2])

    print_sets(sets)

    solve()

