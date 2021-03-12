from jobshop.Instance import Instance
from jobshop.Result import Result, ExitCause
from jobshop.Solver import Solver
from jobshop.encodings.JobNumbers import JobNumbers


class BasicSolver(Solver):
    def __init__(self):
        pass

    def solve(self, instance, deadline=None):
        sol = JobNumbers(instance)
        for t in range(instance.numTasks):
            for j in range(instance.numJobs):
                sol.jobs[sol.nextToSet]= j
                sol.nextToSet += 1
        return Result(instance, sol.toSchedule(), ExitCause.Blocked), sol


if __name__ == '__main__':
    import logging
    from jobshop.Schedule import Schedule
    basic_solver = BasicSolver()
    instance = Instance().fromFile("../../tests/instances/la08")
    result, sol = basic_solver.solve(instance=instance, deadline=None)
    assert True == isinstance(instance, Instance)
    assert result.instance is not None
    assert True == isinstance(result.schedule, Schedule)
    assert True == isinstance(result.instance, Instance)
    assert sol is not None
    print("sol:", sol)
    print("result.schedule.makespan:", result.schedule.makespan())
    print("result.instance:", result.instance.numJobs, result.instance.numTasks)