N = 3



def clone_grid(g):
    new = []
    for l in g:
        new.append([l[i] for i in l])
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

    print_grid(pos)

    for i in range(0, N * N):
        for j in range(0, N * N):
            if g[i][j] != 0:
                pos[i][j] = str(g[i][j])
                propagate(pos, i, j)

    return pos


def propagate(pos, i0, j0):
    # print(f"PROPAGATING {i0} {j0}")


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
            i = 3 * si + di
            j = 3 * sj + dj
            if i != i0 and j != j0 and c in pos[i][j]:
                pos[i][j] = pos[i][j].replace(c, '')
                propagate(pos, i, j)




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





