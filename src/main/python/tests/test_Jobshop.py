import unittest
import numpy as np
import logging
from jobshop.Instance import Instance
from jobshop.encodings.ResourceOrder import ResourceOrder
from jobshop.Schedule import Schedule
from jobshop.solvers.BasicSolver import BasicSolver
from jobshop.encodings.Task import Task
from jobshop.solvers.GreedySolver import GreedySolver


instance_path = "instances/aaa1"
testing_instance = Instance().fromFile(instance_path)


class ResourceOrderTestCase(unittest.TestCase):
    def setup_class(self):
        self.instance = testing_instance
        self.ROObject = ResourceOrder(instance=Schedule(pb=self.instance, times=self.instance.durations))

    def test_init(self):
        self.assertEqual(2, self.instance.numJobs)
        self.assertEqual(3, self.instance.numTasks)
        self.assertEqual(True, isinstance(self.instance, Instance))
        self.assertEqual(True, isinstance(self.ROObject, ResourceOrder))
        self.assertListEqual([0., 1., 2.], list(self.ROObject.instance.machines[0]))
        self.assertListEqual( [1., 0., 2.], list(self.ROObject.instance.machines[1]))
        self.assertEqual("(1, 1)", str(self.ROObject.tasksByMachine[0][0]))
        self.assertEqual("(0, 0)", str(self.ROObject.tasksByMachine[0][1]))
        self.assertEqual("(1, 0)", str(self.ROObject.tasksByMachine[1][0]) )
        self.assertEqual("(0, 1)", str(self.ROObject.tasksByMachine[1][1]))
        self.assertEqual("(0, 2)", str(self.ROObject.tasksByMachine[2][0]) )
        self.assertEqual("(1, 2)", str(self.ROObject.tasksByMachine[2][1]))

    def test_to_schedule(self):
        schedule = self.ROObject.toschedule()
        self.assertEqual(True, isinstance(schedule, Schedule))
        self.assertEqual(16, schedule.makespan())
        self.assertEqual(2, schedule.pb.numJobs)
        self.assertEqual(3, schedule.pb.numTasks)

    def test_copy(self):
        CopyROObject = self.ROObject.copy()
        logging.warning(str(CopyROObject))
        self.assertEqual(True, isinstance(self.ROObject.copy(), ResourceOrder))
        self.assertEqual(str(CopyROObject.tasksByMachine[0][0]), str(self.ROObject.tasksByMachine[0][0]))
        self.assertEqual(str(CopyROObject.tasksByMachine[0][1]), str(self.ROObject.tasksByMachine[0][1]))
        self.assertEqual(str(CopyROObject.tasksByMachine[1][0]), str(self.ROObject.tasksByMachine[1][0]) )
        self.assertEqual(str(CopyROObject.tasksByMachine[1][1]), str(self.ROObject.tasksByMachine[1][1]))
        self.assertEqual(str(CopyROObject.tasksByMachine[2][0]), str(self.ROObject.tasksByMachine[2][0]) )
        self.assertEqual(str(CopyROObject.tasksByMachine[2][1]), str(self.ROObject.tasksByMachine[2][1]))

    def test_display(self):
        logging.warning(self.ROObject)
        self.assertEqual(True, True)


class ScheduleTestCase(unittest.TestCase):
    def setup_class(self):
        self.instance = testing_instance
        self.schedule = Schedule(self.instance, times=self.instance.durations)

    def test_init(self):
        pass

    def test_startTime(self):
        pass

    def test_isValid(self):
        pass

    def test_makespan(self):
        self.assertEqual(16, self.schedule.makespan())
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

    def not_test_solve(self):
        result, sol = self.basic_solver.solve(instance=self.instance, deadline=None)
        self.assertEqual(True, isinstance(self.instance, Instance))
        self.assertNotEqual(result.instance, None)
        self.assertEqual(True, isinstance(result.schedule, Schedule))
        self.assertEqual(True, isinstance(result.instance, Instance))
        self.assertNotEqual(sol, None)
        self.assertEqual(12, result.schedule.makespan())
        self.assertEqual(6, result.schedule.endTime(Task(job=0, task=1)))
        self.assertEqual(3, result.schedule.startTime(job=1, task=1))
        self.assertEqual(0, result.schedule.criticalPath())
        logging.warning("sol:" + str(sol))
        logging.warning("result.schedule:" + str(result.schedule))
        logging.warning("result.instance:" + str(result.instance))
        logging.warning(result)


class GreedySolverTestCase(unittest.TestCase):
    def setup_class(self):
        self.solver = GreedySolver(instance_path)

    def test_spt_solver(self):
        self.solver.runSPT()
        logging.warning("***************************************************************")
        logging.warning(str(self.solver.resource_order))
        logging.warning("***************************************************************")
        logging.warning("makespan:"+ str(self.solver.schedule.makespan()))
        logging.warning(self.solver.instance.durations)
        logging.warning(self.solver.schedule.makespan())
        logging.warning(self.solver.resource_order.instance.machines)
        self.assertEqual(True, False)

if __name__ == '__main__':
    print(testing_instance)
    #unittest.main()
