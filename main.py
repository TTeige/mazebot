import requests
import json
import sys
import math
import datetime
from collections import namedtuple


def run():
    start, end, maze, maze_name = get_maze()
    solved = a_star(start, end, maze)
    print(solved)
    print(check_solution(maze_name, solved))


def json_to_obj(data):
    return json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


def race():
    req = requests.post('https://api.noopschallenge.com/mazebot/race/start', data=json.dumps({'login': 'tteige'}))
    name = json_to_obj(req.content).nextMaze
    print(name)
    while name != "":
        start, end, maze, maze_name = get_maze(name)
        solved = a_star(start, end, maze)
        # print(solved)
        name = check_race_solution(name, solved)
        print(name)


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
    # for m in maze:
    #     print(m)

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
            # for p in rec:
            #     maze[p[1]][p[0]] = "P"
            # for m in maze:
            #     print(m)
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


def get_maze(name="/mazebot/random"):
    req = requests.get('https://api.noopschallenge.com' + name)
    if req.status_code != 200:
        print("Status code error - " + str(req.status_code) + " when getting maze")
        exit(1)
    x = json_to_obj(req.content)
    return x.startingPosition, x.endingPosition, x.map, x.mazePath


def convert(l):
    s = [str(i) for i in l]
    res = "".join(s)

    return res


def check_solution(name, path):
    req = requests.post('https://api.noopschallenge.com' + name, data=json.dumps({
        'directions': path
    }))
    print(req.status_code)
    print(req.json())
    return req.status_code == 200


def check_race_solution(name, path):
    req = requests.post('https://api.noopschallenge.com' + name, data=json.dumps({
        'directions': path
    }))
    if req.status_code != 200:
        print("Status code error - " + str(req.status_code) + " when getting maze")
        print(req.json())
        print(req)
        exit(1)
    resp = json_to_obj(req.content)
    if hasattr(resp, 'nextMaze'):
        return json_to_obj(req.content).nextMaze
    else:
        print(req.json())
        print(req)
    exit(1)


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'race':
            race()
    else:
        run()
