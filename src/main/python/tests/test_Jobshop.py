import unittest
import numpy as np
from jobshop.Instance import Instance
from jobshop.encodings.ResourceOrder import ResourceOrder
from jobshop.Schedule import Schedule


class ResourceOrderTestCase(unittest.TestCase):
    def setup_class(self):
        self.instance = Instance.fromFile("instances/aaa1")
        self.ROObject = ResourceOrder(self.instance)
        self.schedule = self.ROObject.toschedule()

    def test_init(self):
        self.assertEqual(2, self.instance.numJobs)
        self.assertEqual(3, self.instance.numTasks)
        self.assertEqual(True, isinstance(self.instance, Instance))
        self.assertEqual(True, isinstance(self.ROObject, ResourceOrder))

    def test_to_schedule(self):
        self.assertEqual(True, isinstance(self.schedule, Schedule))



    def test_copy(self):
        CopyROObject = self.ROObject.copy()
        self.assertEqual(type(CopyROObject), type(self.schedule))

    def test_display(self):
        print(self.ROObject)
        self.assertEqual(True, True)


class ScheduleTestCase(unittest.TestCase):
    def setup_class(self):
        self.instance = Instance.fromFile("instances/aaa1")
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


if __name__ == '__main__':
    unittest.main()
