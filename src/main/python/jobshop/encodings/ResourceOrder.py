import copy
import logging
from jobshop.Encoding import *
from jobshop.Schedule import *
from jobshop.Instance import Instance


class ResourceOrder(Encoding):
    def __init__(self, instance):
        super(Encoding, self).__init__()
        self.instance = instance
        super(Instance)
        if isinstance(self.instance, Instance):
            tasks_on_machine   = [None for _ in range(instance.numJobs)]  # or 0 or Task(0, 0)
            self.tasksByMachine = [tasks_on_machine for _ in range(instance.numMachines)]
            self.nextFreeSlot  = [0]*instance.numMachines

        elif isinstance(self.instance, Schedule):
            pb = self.instance.pb
            self.tasksByMachine = [[]]*pb.numMachines # or 0 !!!!!!!!!!!!!!!
            self.nextFreeSlot = [0]*pb.numMachines

            # for this machine, find all tasks that are executed on it and sort them by their start time
            for m in range(pb.numMachines):
                task_list_on_machine = [Task(job, pb.task_with_machine(job=job, wanted_machine=m)) for job in range(pb.numJobs) ]
                task_list_on_machine = list(sorted(task_list_on_machine, key=lambda t: self.instance.startTime(t.job, t.task)))  # sorted by start time
                self.tasksByMachine[m] = task_list_on_machine
                # indicate that all tasks have been initialized for machine m
                self.nextFreeSlot[m] = pb.numJobs
            self.instance = self.instance.pb
        else:
            self.instance = None
            logging.error("Unknown instance type")
            exit()

    def toschedule(self):
        # indicate for each task that have been scheduled, its start time
        startTimes = [[0]*self.instance.numTasks for _ in range(self.instance.numJobs)]

        # for each job, how many tasks have been scheduled (0 initially)
        nextToScheduleByJob = [0]*self.instance.numJobs

        # for each machine, how many tasks have been scheduled (0 initially)
        nextToScheduleByMachine = [0]*self.instance.numMachines

        # for each machine, earliest time at which the machine can be used
        releaseTimeOfMachine = [0]*self.instance.numMachines
        number_of_scheduled_task = 0
        any_match = True
        while any_match:
            schedulable = None
            tasks_that_are_next_to_schedule = [self.tasksByMachine[m][nextToScheduleByMachine[m]] for m in range(self.instance.numMachines) if nextToScheduleByMachine[m] < self.instance.numJobs ]
            for mtask in tasks_that_are_next_to_schedule:
                if mtask.task == nextToScheduleByJob[mtask.job]:
                    schedulable = mtask
                    number_of_scheduled_task += 1
                    break
            if schedulable is not None:
                # we found a schedulable task, lets call it t
                t = schedulable
                machine = int( self.instance.machine(t.job, t.task) )
                if t.task == 0:
                    est = 0
                else:
                    est = startTimes[t.job][t.task-1] + self.instance.duration(t.job, t.task-1)
                index_release = int(self.instance.machine(t))
                est = max(est, releaseTimeOfMachine[index_release])
                startTimes[t.job][t.task] = est

                # mark the task as scheduled
                nextToScheduleByJob[t.job] += 1
                nextToScheduleByMachine[machine] += 1
                # increase the release time of the machine
                releaseTimeOfMachine[machine] = est + self.instance.duration(t.job, t.task)
            else:
                logging.warning("Number of tasks scheduled:" + str(number_of_scheduled_task))
                return None
            any_match_list = [nextToScheduleByJob[j] < self.instance.numTasks for j in range(self.instance.numJobs) ]
            any_match = True in any_match_list

        # we exited the loop : all tasks have been scheduled successfully
        logging.warning("Number of tasks scheduled:" + str(number_of_scheduled_task))
        return Schedule(self.instance, startTimes)

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        s = ""
        for m in range(self.instance.numMachines):
            s += "\nMachine" + str(m) + ":"
            tasks_str = ";".join([str(self.tasksByMachine[m][job]) for job in range(self.instance.numJobs)] ) #join tasks or machine m
            s += tasks_str + "\n"
        return s