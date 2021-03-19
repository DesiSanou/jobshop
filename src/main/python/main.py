import time
from tabulate import tabulate
import argparse
from jobshop.Solver import *
from jobshop.solvers.GreedySolver import GreedySolver
from jobshop.solvers.BasicSolver import BasicSolver
from jobshop.Instance import Instance
from jobshop.encodings.ResourceOrder import ResourceOrder

bestKnown = {"la01": 666,
             "la02": 655,
             "aaa1": 11,
             "ft06": 55,
             "ft10": 930,
             "ft20": 1165
             }


def format_result(solve, instance, start):
    makespan = solve.toSchedule().makespan()
    best = bestKnown[instance]
    ecart = round(100 * (makespan - best) / best, 1)
    size = str(solve.instance.numJobs) + "x" + str(solve.instance.numTasks)
    runtime = time.time() - start

    return size, best, round(runtime, 2), makespan, ecart


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--instances', default=None, type=str)
    args = parser.parse_args()
    instances = args.instances.split('-')
    results = []

    results = []
    print('\n')
    print('Basic Result : \n')
    for inst in instances:
        try:
            instance = Instance.fromFile('tests/instances/' + inst)
        except(FileNotFoundError, IOError):
            print('File not found')
        start = time.time()
        result, sol_basic = BasicSolver().solve(instance=instance, deadline=None)
        response = format_result(sol_basic, inst, start)

        results.append([inst, response[0], response[1], response[2], response[3], response[4]])
    print(tabulate(results, headers=['instance', 'size', 'best', 'runtime', 'makespan', 'ecart']))

    print('SPT Result : \n')
    for inst in instances:
        print(inst)
        try:
            instance = Instance.fromFile('tests/instances/' + inst)
        except(FileNotFoundError, IOError):
            print('File not found')
        start = time.time()
        inst_path = 'tests/instances/' + inst
        greedy_solver = GreedySolver(instance_path=inst_path)
        greedy_solver.runSPT()
        response = format_result(greedy_solver.resource_order, inst, start)

        results.append([inst, response[0], response[1], response[2], response[3], response[4]])
    print(tabulate(results, headers=['instance', 'size', 'best', 'runtime', 'makespan', 'ecart']))

