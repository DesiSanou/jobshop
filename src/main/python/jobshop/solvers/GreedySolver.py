import copy
import logging

from jobshop.Instance import Instance
from jobshop.encodings.ResourceOrder import ResourceOrder, Task
from jobshop.Schedule import Schedule


class GreedySolver:
    def __init__(self, instance_path):
        self.instance = Instance.fromFile(instance_path)
        self.resource_order = ResourceOrder(instance=Schedule(pb=self.instance,
                                                              times=self.instance.durations))

    def runSPT(self):
        for machine in range(len(self.resource_order.tasksByMachine)):
            tasks_to_schedule_on_machine = self.resource_order.tasksByMachine[machine].copy()
            sorted_duration_list = [self.instance.duration(t) for t in tasks_to_schedule_on_machine]
            sorted_duration_list.sort(reverse=True)
            scheduled_tasks = list()
            while len(scheduled_tasks) < len(tasks_to_schedule_on_machine):
                for task in tasks_to_schedule_on_machine:
                    if self.instance.duration(task) == sorted_duration_list[-1]:
                        sorted_duration_list.pop(-1)
                        scheduled_tasks.append(task)
            self.resource_order.tasksByMachine[machine] = scheduled_tasks
            return self.resource_order

    def runLRPT(self):
        makespan = self.resource_order.toschedule().makespan()
        for machine in range(len(self.resource_order.tasksByMachine)):
            tasks_to_schedule_on_machine = self.resource_order.tasksByMachine[machine].copy()
            sorted_duration_list = [self.instance.duration(t) for t in tasks_to_schedule_on_machine]
            sorted_duration_list.sort()
            scheduled_tasks = list()
            while len(scheduled_tasks) < len(tasks_to_schedule_on_machine):

                for task in tasks_to_schedule_on_machine:
                    if self.instance.duration(task) == sorted_duration_list[-1]:
                        sorted_duration_list.pop(-1)
                        scheduled_tasks.append(task)
            self.resource_order.tasksByMachine[machine] = scheduled_tasks
        logging.warning("LRPT makespan:"+str(makespan))

