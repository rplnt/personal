from libcpp.vector cimport vector
from libcpp.map cimport map

import random
import time

DEF X = 5
DEF Y = 6
DEF BOARD_SIZE = X*Y
DEF COLORS = 4

cdef map[unsigned long long int, int] stateboard
d_stateboard = {}

cdef int collisions = 0
cdef map[int, int] max_score

cdef int[2][4] directions = [[-1, 1, 0, 0], [0, 0, 1, -1]]


def cplay(board=None, result=None):
    cdef int[X][Y] _board
    if not board:
        _board = get_board()
    else:
        _board = board
    reset_globals()

    t0 = time.time()
    play(_board, 0, 0)
    t = time.time() - t0

    if result == 'board':
        return t, board
    elif result == 'scores':
        return t, get_scores()
    elif result == 'satatecount':
        return t, get_state_count()
    else:
        return t, None


cdef play(int[X][Y] board, int depth, int score):
    groups = get_groups(board)
    if len(groups) == 0:
        # if d_check_for_collisions(board, score):
        #     return
        if max_score[score]:
            max_score[score] += 1
        else:
            # print 'New score: {:<4} (out of {} finished games)'.format(score, sum(max_score.values()) + 1)
            max_score[score] = 1
        return

    if d_check_for_collisions(board, score):
        return

    cdef int total = 0
    cdef int[X][Y] group_board, shifted

    for group in groups:  # strategy(groups):
        # if depth == 0:
        #     print 'Starting new branch {}: {}'.format(group.values()[0], [(c%(X+Y), c/(X+Y)) for c in group.keys()])
        group_board = clone_board(board)

        # remove tiles
        for pos_code in group:
            x = pos_code % (X+Y)
            y = pos_code / (X+Y)
            group_board[x][y] = 0

        group_score = score + count_score(len(group))

        for i in range(4):
            shifted = clone_board(group_board)
            shift_board(shifted, directions[0][i], directions[1][i])
            play(shifted, depth + 1, group_score)


def strategy(groups):
    for group in sorted(groups, key=len):
        yield group


cdef clone_board(int[X][Y] board):
    cdef int[X][Y] new_board

    for x in range(X):
        for y in range(Y):
            new_board[x][y] = board[x][y]

    return new_board


def get_board():
    source = [[random.randint(1, COLORS) for x in range(Y)] for y in range(X)]

    cdef int[X][Y] board

    for x in range(X):
        for y in range(Y):
            board[x][y] = source[x][y]

    return board


cdef int is_over(int x, int y):
    # cdef int x, y = pos
    return x >= X or x < 0 or y >= Y or y < 0


def get_hash(board):
    cdef int[X][Y] cboard
    for y in range(Y):
        for x in range(X):
            cboard[x][y] = board[x][y]

    return hash_board(cboard)


cdef hash_board(int[X][Y] board):
    cdef unsigned long long h = 0
    cdef short int value
    for y in range(Y):
        for x in range(X):
            value = board[x][y]
            h |= value
            h = h << 3  # max 7 colors
    return h

cdef int count_score(int selected):
    return selected * selected - 4 * selected + 6


cdef move_tile(int[X][Y] board, int px, int py, int dx, int dy):
    if is_over(px, py):
        return

    if board[px][py] == 0:
        return

    cdef int npx = px + dx
    cdef int npy = py + dy

    if is_over(npx, npy):
        return

    if board[npx][npy] == 0:
        board[npx][npy] = board[px][py]
        board[px][py] = 0
        move_tile(board, npx, npy, dx, dy)


cdef shift_board(int[X][Y] board, int dx, int dy):
    # left  = Point(-1, 0)
    if dx == -1 and dy == 0:
        outer = range(1, X)
        inner = range(0, Y)

    # right = Point(1, 0)
    if dx == 1 and dy == 0:
        outer = range(X-1, -1, -1)
        inner = range(0, Y)

    # up    = Point(0, 1)
    if dx == 0 and dy == 1:
        outer = range(Y-1, -1, -1)
        inner = range(0, X)

    # down  = Point(0, -1)
    if dx == 0 and dy == -1:
        outer = range(1, Y)
        inner = range(0, X)

    for o in outer:
        for i in inner:
            # if direction in [up, down]:
            if (dx == 0 and dy == 1) or (dx == 0 and dy == -1):
                move_tile(board, i, o, dx, dy)
            else:
                move_tile(board, o, i, dx, dy)


cdef get_groups(int[X][Y] board):
    groups = []
    selected = {}

    for y in range(Y):
        for x in range(X):
            new_group = {}
            select_group(board, x, y, new_group, board[x][y])
            if len(new_group) > 1:
                if new_group.keys()[0] in selected:
                    continue
                else:
                    for key in new_group:
                        selected[key] = 1
                    groups.append(new_group)
                    # TODO: maybe create already modified copies here?

    return groups


cdef select_group(int[X][Y] board, int px, int py, group, int color):
    if color == 0:
        return
    if is_over(px, py):
        return

    pos_code = px + py * (X+Y)
    # if board[px][py] == color and (px, py) not in group:
    if board[px][py] == color and not pos_code in group:
        # group[(px, py)] = color
        group[pos_code] = color
    else:
        return

    select_group(board, px - 1, py + 0, group, color)
    select_group(board, px + 1, py + 0, group, color)
    select_group(board, px + 0, py + 1, group, color)
    select_group(board, px + 0, py - 1, group, color)


# dictionary version
cdef int d_check_for_collisions(int[X][Y] board, int score):
    cdef unsigned long long board_id = hash_board(board)
    if board_id in d_stateboard and score <= d_stateboard[board_id]:
        global collisions
        collisions += 1
        return 1
    else:
        d_stateboard[board_id] = score
        return 0

# map version
cdef int check_for_collisions(int[X][Y] board, int score):
    cdef unsigned long long board_id = hash_board(board)
    if stateboard[board_id] and score <= stateboard[board_id]:
        global collisions
        collisions += 1
        return 1
    else:
        stateboard[board_id] = score
        return 0


def print_game_stats(print_scores=True):
    print 'game states: {}|{}'.format(len(d_stateboard), len(stateboard))
    print 'collisions: {}'.format(collisions)
    print 'scores:',

    total = 0
    if print_scores:
        print
        for k in sorted(max_score.keys(), reverse=True):
            print '{} ({})'.format(k, max_score[k])
            total += max_score[k]
    else:
        print sorted(max_score.keys(), reverse=True)
        total = len(max_score)

    print 'finished games: {}'.format(total)


def get_scores():
    return max_score.keys()


def get_state_count():
    return len(d_stateboard) + len(stateboard)


cdef reset_globals():
    global collisions
    collisions = 0

    global d_stateboard
    d_stateboard = {}

    global stateboard
    stateboard.clear()

    global max_score
    max_score.clear()
