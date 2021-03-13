import copy
import logging

from jobshop.Instance import Instance
from jobshop.encodings.ResourceOrder import ResourceOrder, Task
from jobshop.solvers.BasicSolver import BasicSolver
from jobshop.Schedule import Schedule


class GreedySolver:

    def __init__(self, instance_path):
        self.instance = Instance.fromFile(instance_path)
        self.schedule = Schedule(pb=self.instance, times=self.instance.durations)
        self.resource_order = ResourceOrder(instance=self.schedule)

    def runSPT(self):
        tasks_on_mach = copy.deepcopy(self.resource_order.tasksByMachine)
        for i in range(len(tasks_on_mach)):
            tasks_on_mach[i] = sorted(tasks_on_mach[i], key=lambda t: self.instance.duration(t))
            tasks_on_mach[i] = list(tasks_on_mach[i])
        print(tasks_on_mach, "\n", self.resource_order.tasksByMachine)
        self.resource_order.tasksByMachine = tasks_on_mach

    def runLRPT(self):
        pass