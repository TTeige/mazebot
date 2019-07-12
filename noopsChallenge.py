import requests
import json
from misc import json_to_obj


class NoopsChallenge:

    def __init__(self, algorithm):
        self.base_path = 'https://api.noopschallenge.com'
        self.algorithm = algorithm

    def check_solution(self, name, path):
        req = requests.post(self.base_path + name, data=json.dumps({
            'directions': path
        }))
        print(req.status_code)
        print(req.json())
        return req.status_code == 200

    def check_race_solution(self, name, path):
        req = requests.post(self.base_path + name, data=json.dumps({
            'directions': path
        }))
        if req.status_code != 200:
            print("Status code error - " + str(req.status_code) + " when getting maze")
            print(req.json())
            exit(1)
        resp = json_to_obj(req.content)
        if hasattr(resp, 'nextMaze'):
            return json_to_obj(req.content).nextMaze
        else:
            print(req.json())
        exit(1)

    def race(self):
        req = requests.post(self.base_path + '/mazebot/race/start', data=json.dumps({'login': 'tteige'}))
        name = json_to_obj(req.content).nextMaze
        print(name)
        while name != "":
            start, end, maze, maze_name = self.get_maze(name)
            solved = self.algorithm(start, end, maze)
            name = self.check_race_solution(name, solved)
            print(name)

    def get_maze(self, name="/mazebot/random"):
        req = requests.get(self.base_path + name)
        if req.status_code != 200:
            print("Status code error - " + str(req.status_code) + " when getting maze")
            exit(1)
        x = json_to_obj(req.content)
        return x.startingPosition, x.endingPosition, x.map, x.mazePath

    def run(self):
        start, end, maze, maze_name = self.get_maze()
        solved = self.algorithm(start, end, maze)
        print(solved)
        self.check_solution(maze_name, solved)
