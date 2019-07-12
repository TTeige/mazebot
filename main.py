import sys

from noopsChallenge import NoopsChallenge
from a_star import a_star


def algs(x):
    return {
        'a_star': a_star
    }.get(x)


def start_maze(run_mode, algorithm_type):
    np = NoopsChallenge(algs(algorithm_type))
    if run_mode == "random":
        np.run()
    else:
        np.race()


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) != 3:
        print("Provide algorithm and type")
        exit(1)
    start_maze(sys.argv[1], sys.argv[2])
