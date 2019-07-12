import datetime
import math
import sys


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def a_star(start, end, maze):
    print("Begins: " + str(start[0]) + ", " + str(start[1]))
    print("Ends: " + str(end[0]) + ", " + str(end[1]))
    closed_set = {None}
    closed_set.remove(None)
    open_set = {(start[0], start[1])}
    came_from = {}
    g_score = {}
    f_score = {}
    for idx_y, y in enumerate(maze):
        for idx_x, x in enumerate(y):
            g_score[(idx_x, idx_y)] = sys.maxsize
            f_score[(idx_x, idx_y)] = sys.maxsize

    g_score[(start[0], start[1])] = 0
    f_score[(start[0], start[1])] = heuristic(start, end)

    start_time = datetime.datetime.now()

    while len(open_set) > 0:
        lowest = None
        for o in open_set:
            if lowest is None:
                lowest = o
            if f_score[o] < f_score[lowest]:
                lowest = o
        current = lowest

        if current[0] == end[0] and current[1] == end[1]:
            print(datetime.datetime.now() - start_time)
            rec = reconstruct_path(came_from, current)
            print("We did it!")
            print(len(maze))
            print(len(maze[0]))
            for p in rec:
                maze[p[1]][p[0]] = "O"
            for m in maze:
                print(m)

            return get_direction_list(rec)

        open_set.remove(current)
        closed_set.add(current)
        neighbours = get_neighbours(current, len(maze), len(maze[0]), maze)
        for neighbour in neighbours:
            if neighbour in closed_set:
                continue
            t_g_score = g_score[current] + 1

            if neighbour not in open_set:
                open_set.add(neighbour)
            elif t_g_score >= g_score[neighbour]:
                continue

            came_from[neighbour] = current
            g_score[neighbour] = t_g_score
            f_score[neighbour] = g_score[neighbour] + heuristic(neighbour, end)

        if len(open_set) == 0:
            print("No solution")
            return


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path


def get_neighbours(loc, w, h, maze):
    neighbours = []
    if loc[0] != 0:
        neighbours.append((loc[0] - 1, loc[1]))
    if loc[0] != w - 1:
        neighbours.append((loc[0] + 1, loc[1]))
    if loc[1] != 0:
        neighbours.append((loc[0], loc[1] - 1))
    if loc[1] != h - 1:
        neighbours.append((loc[0], loc[1] + 1))

    to_remove = []
    for n in neighbours:
        if maze[n[1]][n[0]] == 'X':
            to_remove.append(n)

    neighbours = [x for x in neighbours if x not in to_remove]

    return neighbours


def get_direction_list(path):
    path.reverse()
    directions = []
    for i, p in enumerate(path):
        if i == len(path) - 1:
            break
        if p[0] < path[i + 1][0]:
            directions.append("E")
        elif p[0] > path[i + 1][0]:
            directions.append("W")
        elif p[1] < path[i + 1][1]:
            directions.append("S")
        elif p[1] > path[i + 1][1]:
            directions.append("N")

    return convert(directions)


def heuristic(a, b):
    return math.sqrt(math.pow(a[0] + b[0], 2) + math.pow(a[1] + b[1], 2))


def convert(l):
    s = [str(i) for i in l]
    res = "".join(s)
    return res
