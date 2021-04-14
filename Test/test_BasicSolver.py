import unittest
import logging

from jobshop.Instance import Instance
from jobshop.Schedule import Schedule
from jobshop.solvers.BasicSolver import BasicSolver
from jobshop.encodings.Task import Task



class BasicSolverTestCase(unittest.TestCase):
    def setup_class(self):
        self.instance = Instance.fromFile("../jobshop/instances/abz5")
        self.basic_solver = BasicSolver()

    def test_solve(self):
        result, sol = self.basic_solver.solve(instance=self.instance, deadline=None)
        self.assertEqual(True, isinstance(self.instance, Instance))

        self.assertNotEqual(result.instance, None)
        self.assertEqual(True, isinstance(result.schedule, Schedule))
        self.assertEqual(True, isinstance(result.instance, Instance))
        self.assertNotEqual(sol, None)
        self.assertEqual(12, result.schedule.makespan())
        self.assertEqual(6, result.schedule.endTime(Task(job=0,task=1)))
        self.assertEqual(0, result.schedule.startTime())
        self.assertEqual(0, result.schedule.criticalPath())
        logging.warning("sol:" + str(sol))
        logging.warning("result.schedule:" + str(result.schedule))
        logging.warning("result.instance:" + str(result.instance))
        logging.warning(result)


if __name__ == '__main__':
    unittest.main()

