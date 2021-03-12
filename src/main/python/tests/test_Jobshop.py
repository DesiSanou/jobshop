import unittest
import numpy as np
import logging
from jobshop.Instance import Instance
from jobshop.encodings.ResourceOrder import ResourceOrder
from jobshop.Schedule import Schedule
from jobshop.solvers.BasicSolver import BasicSolver
from jobshop.encodings.Task import Task

testing_instance = Instance().fromFile("instances/aaa1")


class ResourceOrderTestCase(unittest.TestCase):
    def setup_class(self):
        self.instance = testing_instance
        self.ROObject = ResourceOrder(self.instance)
        self.schedule = self.ROObject.toschedule()

    def test_init(self):
        self.assertEqual(2, self.instance.numJobs)
        self.assertEqual(3, self.instance.numTasks)
        self.assertEqual(True, isinstance(self.instance, Instance))
        self.assertEqual(True, isinstance(self.ROObject, ResourceOrder))

    def test_to_schedule(self):
        self.assertEqual(True, isinstance(self.schedule, Schedule))
        self.assertEqual(12, self.schedule.makespan())
        self.assertEqual(2, self.schedule.pb.numJobs)
        self.assertEqual(3, self.schedule.pb.numTasks)

    def test_copy(self):
        CopyROObject = self.ROObject.copy()
        self.assertEqual(type(CopyROObject.toSchedule()), type(self.schedule))
        self.assertEqual(12, CopyROObject.makespan() )

    def test_display(self):
        print(self.ROObject)
        self.assertEqual(True, True)


class ScheduleTestCase(unittest.TestCase):
    def setup_class(self):
        self.instance = testing_instance
        startTimes = np.zeros((self.instance.numJobs,  self.instance.numTasks))
        self.schedule = Schedule(self.instance, startTimes)

    def test_init(self):
        pass

    def test_startTime(self):
        pass

    def test_isValid(self):
        pass

    def test_makespan(self):
        pass

    def test_endTime(self):
        pass

    def test_isCriticalPath(self):
        pass

    def test_criticalPath(self):
        pass


class BasicSolverTestCase(unittest.TestCase):
    def setup_class(self):
        self.instance = testing_instance
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
    print(testing_instance)
    #unittest.main()
