import unittest
from jobshop.Instance import Instance
from jobshop.Schedule import Schedule
import numpy as np

from jobshop.encodings.Task import Task


class ScheduleTestCase(unittest.TestCase):
    
    def setup_class(self):
        self.instance = Instance.fromFile("../jobshop/instances/abz8")
        startTimes = np.zeros((self.instance.numJobs, self.instance.numTasks))
        self.ScheduleObject = Schedule(self.instance, startTimes)




    def test_init(self):
        self.assertEqual(True, isinstance(self.ScheduleObject, Schedule))

    def test_isvalid(self):
        valid = self.ScheduleObject.isValid()
        self.assertEqual(False, valid)
        
    def test_makeSpan(self):
        span = self.ScheduleObject.makespan()
        self.assertEqual(span, 107)

    def test_isCriticalPath(self):
        task = []
        task.append(Task(5, 5))
        task.append(Task(7, 7))
        isCritical = self.ScheduleObject.isCriticalPath(task)
        self.assertEqual(False, isCritical)


if __name__ == '__main__':
    unittest.main()
