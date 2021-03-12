import logging
from jobshop.Encoding import Encoding
from jobshop.Instance import Instance
from jobshop.Schedule import Schedule
from jobshop.encodings.Task import Task

class JobNumbers(Encoding):
    def __init__(self, intance_or_schedule):
        self.nextToSet = 0
        self.instance = intance_or_schedule
        if isinstance(self.instance, Instance):
            super(Instance)
            self.jobs = [-1]*(self.instance.numJobs * self.instance.numMachines)
        elif isinstance(intance_or_schedule, Schedule):
            self.schedule = intance_or_schedule
            super(Instance)
            self.instance = self.schedule.pb
            self.jobs = [0]*(self.instance.numJobs * self.instance.numTasks)
            nextOnJob = [0]*self.instance.numJobs
            task_list = list()
            any_match = True
            while any_match:
                for j in range(self.instance.numJobs):
                    t = Task(j, nextOnJob[j])
                    if t.task < self.instance.numTasks:
                        task_list.append(t)
                sorted_task_list = sorted(task_list, key=self.schedule.startTime)
                next = sorted_task_list[0]
                self.jobs[self.nextToSet] = next.job
                self.nextToSet += 1
                nextOnJob[next.job] += 1
                any_match_list = [t < self.instance.numTasks for t in nextOnJob]
                any_match = True in any_match_list
        else:
            logging.error("Unknown instance type")

    def toSchedule(self):
        nextFreeTimeResource = [0]* self.instance.numMachines
        nextTask = [0] * self.instance.numJobs
        taskList = [0] * self.instance.numTasks
        startTimes = [taskList for _ in range(self.instance.numJobs)]
        for job in self.jobs:
            task = nextTask[job]
            machine = int(self.instance.machine(job, task))

            est = 0 if task == 0 else startTimes[job][task-1] + self.instance.duration(job, task-1)
            est = max(est, nextFreeTimeResource[machine])

            startTimes[job][task] = est
            nextFreeTimeResource[machine] = est + self.instance.duration(job, task)
            nextTask[job] = task + 1
        return Schedule(self.instance, startTimes)

    def __str__(self):
        return str(self.jobs[0:self.nextToSet])