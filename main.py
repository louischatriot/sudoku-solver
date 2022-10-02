import time


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
def search(pos, square, sols):
    if square == N ** 4 - 1:
        sols.append(pos)
        return None
        # return pos   # If propagation was correct this is the solution

    if square >= N ** 4:
        return None

    i = square // N ** 2
    j = square - i * N ** 2

    if len(pos[i][j]) == 0:
        return None   # Should not happen if propagation done well, except if input is buggy

    if len(pos[i][j]) == 1:
        search(pos, square + 1, sols)
        return None

    for c in pos[i][j]:
        _pos = clone_grid(pos)
        _pos[i][j] = c

        if propagate(_pos, i, j) is None:
            continue
            # return None

        res = search(_pos, square + 1, sols)
        # if res is not None:
        #    return res

    return None


# Assumes it gets passed a sudoku grid with positive ints
def check_validity(solved, checksum):
    for i in range(0, N ** 2):
        for j in range(0, N ** 2):
            if type(solved[i][j]) != int:
                return False
            if solved[i][j] < 0 or solved[i][j] > N ** 2:
                return False

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
            if l1[z] != 0 and l1[z] == l1[z - 1]:
                return False

            if l2[z] != 0 and l2[z] == l2[z - 1]:
                return False

            if l3[z] != 0 and l3[z] == l3[z - 1]:
                return False

        if checksum:
            t = N ** 2 * (N ** 2 + 1) / 2

            if sum(l1) != t:
                return False

            if sum(l2) != t:
                return False

            if sum(l3) != t:
                return False

    return True


def check_consistency(puzzle, solved):
    for i in range(0, N ** 2):
        for j in range(0, N ** 2):
            if puzzle[i][j] != 0 and puzzle[i][j] != solved[i][j]:
                return False

    return True


def sudoku_solver(puzzle):
    if check_validity(puzzle, False) is False:
        raise RuntimeError("Invalid input")

    pos = create_possibilities(puzzle)

    sols = []
    search(pos, 0, sols)

    if len(sols) == 1:
        res = sols[0]
        res = list(map(lambda l: list(map(int, l)), res))
        return res
    else:
        raise RuntimeError("No or multiple solutions")

    return None







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

p1 = [[0, 9, 6, 5, 0, 4, 0, 7, 1], [0, 2, 0, 1, 0, 0, 0, 0, 0], [0, 1, 4, 0, 9, 0, 6, 2, 3], [0, 0, 3, 0, 6, 0, 0, 8, 0], [0, 0, 8, 0, 5, 0, 4, 0, 0], [9, 0, 0, 4, 0, 0, 0, 0, 5], [7, 0, 0, 0, 0, 9, 0, 0, 0], [0, 0, 1, 0, 7, 5, 3, 4, 9], [2, 3, 0, 0, 4, 8, 1, 0, 7]]

p10 = [[0, 0, 0, 0, 0, 2, 7, 5, 0], [0, 1, 8, 0, 9, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [4, 9, 0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 0, 0, 0, 0, 0, 8], [0, 0, 0, 7, 0, 0, 2, 0, 0], [0, 0, 0, 0, 3, 0, 0, 0, 9], [7, 0, 0, 0, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0, 0, 8, 0]]

print("===============================================================")

print_grid(puzzle)

start = time.time()

res = sudoku_solver(p10)

duration = time.time() - start
print(f"==> Duration: {duration}")


