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
            tasks_on_machine   = [Task(0, 0) for _ in range(instance.numJobs)]  # or 0
            self.taskByMachine = [tasks_on_machine for _ in range(instance.numMachines)]
            self.nextFreeSlot  = [0]*instance.numMachines

        elif isinstance(self.instance, Schedule):
            pb = instance.pb
            self.taskByMachine = [None]*pb.numMachines # or 0
            self.nextFreeSlot = [0]*instance.numMachines

            # for this machine, find all tasks that are executed on it and sort them by their start time
            for m in range(instance.pb.numMachines):
                machine = m
                task_list_on_machine = list()
                for job in range(pb.numJobs):
                    # all tasks on this machine (one per job)
                    task_list_on_machine.append(Task(job, pb.task_with_machine(job, machine)))
                task_list_on_machine.sort(key=self._start_time)  # sorted by start time
                self.tasksByMachine[m] = task_list_on_machine
                # indicate that all tasks have been initialized for machine m
                self.nextFreeSlot[m] = instance.numJobs
        else:
            self.instance = None
            logging.error("Unknown instance type")
            exit()

    def _start_time(self, t):
        return self.instance.startTime(t.job, t.task)

    def toschedule(self):
        # indicate for each task that have been scheduled, its start time
        startTimes = [[None]*self.instance.numTasks for _ in range(self.instance.numJobs)]

        # for each job, how many tasks have been scheduled (0 initially)
        nextToScheduleByJob = [0]*self.instance.numJobs

        # for each machine, how many tasks have been scheduled (0 initially)
        nextToScheduleByMachine = [0]*self.instance.numMachines

        # for each machine, earliest time at which the machine can be used
        releaseTimeOfMachine = [0]*self.instance.numMachines
        number_of_scheduled_task = 0
        total_number_of_tasks = self.instance.numTasks * self.instance.numJobs
        #while number_of_scheduled_task < total_number_of_tasks:
        this_is = True
        while this_is:
            this_is = False
            for job in range(self.instance.numJobs):
                if nextToScheduleByJob[job] < self.instance.numTasks:
                    for m in range(self.instance.numMachines):
                        schedulable = None
                        if nextToScheduleByMachine[m] < self.instance.numJobs:
                            for mtask in self.taskByMachine[m]:
                                if mtask.task == nextToScheduleByJob[mtask.job]:
                                    schedulable = mtask
                                    number_of_scheduled_task += 1
                                    logging.warning("Number of tasks scheduled:" + str(number_of_scheduled_task))
                                    break
                        if schedulable is not None:
                            # we found a schedulable task, lets call it t
                            t = schedulable
                            machine = int(self.instance.machine(t.job, t.task))
                            if t.task == 0:
                                est = 0
                            else:
                                est = startTimes[t.job][t.task-1] + self.instance.duration(t.job, t.task-1)
                            index_release = int(self.instance.machine(t))
                            est = np.max(est, releaseTimeOfMachine[index_release])
                            startTimes[t.job][t.task] = est

                            # mark the task as scheduled
                            nextToScheduleByJob[t.job] += 1
                            nextToScheduleByMachine[machine] += 1
                            # increase the release time of the machine
                            releaseTimeOfMachine[machine] = est + self.instance.duration(t.job, t.task)
                        else:
                            # no tasks are schedulable, there is no solution for this resource ordering
                            #return None
                            pass
                    # we exited the loop : all tasks have been scheduled successfully
        return Schedule(self.instance, startTimes)

    def copy(self):
        return copy.deepcopy(self.toschedule())

    def __str__(self):
        s= ""
        for m in range(self.instance.numMachines):
            s += "Machine" + str(m) + ":"
            tasks_str =";"
            tasks_str.join(str(self.taskByMachine[m])) #join tasks or machine m
            s += tasks_str + "\n"
        return s





