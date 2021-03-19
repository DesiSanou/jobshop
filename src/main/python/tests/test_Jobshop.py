import unittest
import numpy as np
import logging
from jobshop.Instance import Instance
from jobshop.encodings.ResourceOrder import ResourceOrder
from jobshop.Schedule import Schedule
from jobshop.solvers.BasicSolver import BasicSolver
from jobshop.encodings.Task import Task
from jobshop.solvers.GreedySolver import GreedySolver
from tabulate import tabulate

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
        self.assertEqual(True, schedule.isValid() )
        crit_path_task_list = schedule.criticalPath()
        critical_path_task= [str(task) for task in crit_path_task_list]
        logging.warning(critical_path_task)

        wrong_crit_Tasks_List = [Task(0, 0), Task(1, 1), Task(1, 2)]
        self.assertEqual(False, schedule.isCriticalPath(wrong_crit_Tasks_List))

        right_crit_tasks_list = [Task(1, 0), Task(1, 1), Task(0, 0), Task(0, 1), Task(0, 2), Task(1, 2)]
        self.assertEqual(True, schedule.isCriticalPath(right_crit_tasks_list))
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
        self.schedule = Schedule(self.instance,
                                 times=self.instance.durations)

    def test_init(self):
        pass

    def test_startTime(self):
        start_time = self.schedule.startTime(job=0,task=0)
        self.assertEqual(3, start_time)
        start_time2 = self.schedule.startTime(job=1, task=2)
        self.assertEqual(4, start_time2)
        start_time3 = self.schedule.startTime(job=Task(job=0, task=2))
        self.assertEqual(2, start_time3)

    def test_isValid(self):
        isval = self.schedule.isValid()
        self.assertEqual(False, isval)

    def test_makespan(self):
        self.assertEqual(16, self.schedule.makespan())

    def test_endTime(self):
        pass

    def test_isCriticalPath(self):
        wrong_crit_Tasks_List = [ Task(0,0), Task(1,1), Task(1,2)]
        self.assertEqual(False, self.schedule.isCriticalPath(wrong_crit_Tasks_List))
        right_crit_tasks_list = [ Task(0,0), Task(0,1), Task(0,2), Task(1,2)]
        self.assertEqual(True, self.schedule.isCriticalPath(right_crit_tasks_list))

    def test_criticalPath(self):
        crit_path_task_list = self.schedule.criticalPath()
        logging.warning(crit_path_task_list)
        self.assertEqual(True, False)


class BasicSolverTestCase(unittest.TestCase):
    def setup_class(self):
        self.instance = testing_instance
        self.basic_solver = BasicSolver()

    def test_solve(self):
        result, sol = self.basic_solver.solve(instance=self.instance, deadline=None)
        self.assertEqual(True, isinstance(self.instance, Instance))
        self.assertNotEqual(result.instance, None)
        logging.warning("Basic sol:" + str(sol))
        logging.warning("Basic Makespan:" + str(result.schedule.makespan()))
        logging.warning(str(result.instance))
        self.assertEqual(True, isinstance(result.schedule, Schedule))
        self.assertEqual(False, isinstance(result.instance, Instance))
        self.assertNotEqual(sol, None)
        self.assertEqual(12, result.schedule.makespan())
        self.assertEqual(6, result.schedule.endTime(Task(job=0, task=1)))
        self.assertEqual(3, result.schedule.startTime(job=1, task=1))

    def test_too(self):
        self.assertEqual(True, False)


class GreedySolverTestCase(unittest.TestCase):

    def setUp(self):
        self.solver = GreedySolver(instance_path)

    def test_spt_solver(self):
        self.solver.runSPT()
        logging.warning(str(self.solver.resource_order))
        schedule = self.solver.resource_order.toschedule()
        logging.warning("SPT makespan:"+str(schedule.makespan()))
        self.assertEqual(16, schedule.makespan())
        critical_path = schedule.criticalPath()
        logging.warning("Critical Path:" + " -> ".join([str(task) for task in critical_path]))
        self.assertEqual(True, False)

    def not_test_lrpt_solver(self):
        self.solver.runLRPT()
        logging.warning(self.solver.instance.durations)
        self.assertEqual(True, False)


if __name__ == '__main__':
    print(testing_instance)
    #unittest.main()
