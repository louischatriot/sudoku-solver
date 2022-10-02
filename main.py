N = 3

def clone_grid(g):
    new = []
    for l in g:
        new.append([i for i in l])
    return new


def print_grid(g):
    print("=================")
    for l in g:
        print(" ".join(map(str, l)))
    print("=================")
    print("")


def create_possibilities(g):
    pos = []
    for l in g:
        pos.append(['123456789' for n in l])

    for i in range(0, N * N):
        for j in range(0, N * N):
            if g[i][j] != 0:
                pos[i][j] = str(g[i][j])
                propagate(pos, i, j)

    return pos


def propagate(pos, i0, j0):
    if len(pos[i0][j0]) == 0:
        return None   # Not a solution


    if len(pos[i0][j0]) > 1:
        return   # Nothing to propagate, not a single result yet

    c = str(pos[i0][j0])

    # Column
    for i in range(0, N * N):
        if i != i0 and c in pos[i][j0]:
            pos[i][j0] = pos[i][j0].replace(c, '')
            propagate(pos, i, j0)

    # Row
    for j in range(0, N * N):
        if j != j0 and c in pos[i0][j]:
            pos[i0][j] = pos[i0][j].replace(c, '')
            propagate(pos, i0, j)

    # Square
    si = i0 // N
    sj = j0 // N

    for di in range(0, N):
        for dj in range(0, N):
            i = N * si + di
            j = N * sj + dj
            if i != i0 and j != j0 and c in pos[i][j]:
                pos[i][j] = pos[i][j].replace(c, '')
                propagate(pos, i, j)

    return pos


# square between 0 and N ** 4 - 1
def search(pos, square):
    if square == N ** 4 - 1:
        return pos   # If propagation was correct this is the solution

    i = square // N ** 2
    j = square - i * N ** 2

    if len(pos[i][j]) == 0:
        return None   # Should not happen if propagation done well, except if input is buggy

    if len(pos[i][j]) == 1:
        return search(pos, square + 1)

    for c in pos[i][j]:
        _pos = clone_grid(pos)
        _pos[i][j] = c

        if propagate(_pos, i, j) is None:
            return None

        res = search(_pos, square + 1)
        if res is not None:
            return res

    return None


# Assumes it gets passed a sudoku grid with positive ints
def check_validity(solved):
    t = N ** 2 * (N ** 2 + 1) / 2


    for i in range(0, N ** 2):
        l1 = []
        l2 = []
        l3 = []

        si = i // N
        sj = i - si * N

        for j in range(0, N ** 2):
            l1.append(solved[i][j])
            l2.append(solved[j][i])

            oi = j // N
            oj = j - oi * N
            ci = si * N + oi
            cj = sj * N + oj
            l3.append(solved[ci][cj])

        l1 = sorted(l1)
        l2 = sorted(l2)
        l3 = sorted(l3)

        for z in range(1, N ** 2):
            if l1[z] == l1[z - 1]:
                return False

            if l2[z] == l2[z - 1]:
                return False

            if l3[z] == l3[z - 1]:
                return False

        if sum(l1) != t:
            return False

        if sum(l2) != t:
            return False

        if sum(l3) != t:
            return False

    return True


def sudoku_solver(puzzle):
    pos = create_possibilities(puzzle)
    _res = search(pos, 0)

    # Kata expects ints
    res = list(map(lambda l: list(map(int, l)), _res))

    return res





# Tests
puzzle = [
    [0, 0, 6, 1, 0, 0, 0, 0, 8], 
    [0, 8, 0, 0, 9, 0, 0, 3, 0], 
    [2, 0, 0, 0, 0, 5, 4, 0, 0], 
    [4, 0, 0, 0, 0, 1, 8, 0, 0], 
    [0, 3, 0, 0, 7, 0, 0, 4, 0], 
    [0, 0, 7, 9, 0, 0, 0, 0, 3], 
    [0, 0, 8, 4, 0, 0, 0, 0, 6], 
    [0, 2, 0, 0, 5, 0, 0, 8, 0], 
    [1, 0, 0, 0, 0, 2, 5, 0, 0]
]

solution = [
    [3, 4, 6, 1, 2, 7, 9, 5, 8], 
    [7, 8, 5, 6, 9, 4, 1, 3, 2], 
    [2, 1, 9, 3, 8, 5, 4, 6, 7], 
    [4, 6, 2, 5, 3, 1, 8, 7, 9], 
    [9, 3, 1, 2, 7, 8, 6, 4, 5], 
    [8, 5, 7, 9, 4, 6, 2, 1, 3], 
    [5, 9, 8, 4, 1, 3, 7, 2, 6],
    [6, 2, 4, 7, 5, 9, 3, 8, 1],
    [1, 7, 3, 8, 6, 2, 5, 9, 4]
]

print_grid(puzzle)
pos = create_possibilities(puzzle)

print_grid(pos)

"""
pos[3][5] = '6'
propagate(pos, 3, 5)

print_grid(pos)
"""


res = search(pos, 0)

print_grid(res)


toptop = sudoku_solver(puzzle)


print_grid(toptop)


print(check_validity(toptop))

print("===========================================")

bogus = [
    [4, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 8, 5, 0, 0, 0, 0, 4],
    [0, 9, 0, 0, 0, 0, 3, 2, 0],
    [3, 0, 0, 0, 6, 2, 0, 0, 8],
    [0, 0, 0, 1, 0, 8, 0, 0, 0],
    [2, 0, 0, 9, 5, 0, 0, 0, 6],
    [0, 2, 7, 0, 0, 0, 0, 8, 0],
    [6, 0, 0, 0, 0, 5, 9, 0, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 2]
]

print_grid(bogus)

bogres = sudoku_solver(bogus)

print_grid(bogres)

print(check_validity(bogres))


