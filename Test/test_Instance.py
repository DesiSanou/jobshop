import unittest
from jobshop.Instance import Instance

class InstanceTestCase(unittest.TestCase):

    def setup_class(self):
        self.instance = Instance.fromFile("../jobshop/instances/abz5")

    def test_fromFile(self):
        self.assertEqual(True, isinstance(self.instance, Instance))

    def test_duration(self):
        duration = self.instance.duration(1,1)
        self.assertEqual(duration, 50)


if __name__ == '__main__':
    unittest.main()
