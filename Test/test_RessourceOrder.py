import unittest
from jobshop.Instance import Instance
from jobshop.Schedule import Schedule
from jobshop.encodings.ResourceOrder import ResourceOrder


class ResourceOrderTestCase(unittest.TestCase):
    def setup_class(self):
        self.instance = Instance.fromFile("../jobshop/instances/abz8")
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


if __name__ == '__main__':
    unittest.main()
