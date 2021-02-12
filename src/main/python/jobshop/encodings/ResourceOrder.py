import math
import copy
import logging
from Encoding import *
from Task import *
from Schedule import *

class ResourceOrder(Encoding):
	def __init__(self, instance):
		super(Encoding, self).__init__()
		self.instance = instance
		if type(instance)=="instance":
			super(instance)
			tasks_on_machine =[None]*instance.numJobs # or 0
			self.taskByMachine = [tasks_on_machine for _ in range(instance.numMachines)]
			self.nextFreeSlot=[0]*instance.numMachines

		elif type(instance)== "Schedule":
			super(instance.pb)
			pb = instance.pb
			self.taskByMachine=[None]*pb.numMachines # or 0
			self.nextFreeSlot=[0]*instance.numMachines

			# for this machine, find all tasks that are executed on it and sort them by their start time
		     for m in range(instance.pb.numMachines):
				machine = m
				task_list_on_machine= list()
				for job in range(pb.numJobs):
					task_list_on_machine.append(Task(job, pb.task_with_machine(job, machine))) # all tasks on this machine (one per job)
				task_list_on_machine.sort(key=self._start_time) # sorted by start time
				
				self.tasksByMachine[m] = task_list_on_machine
				self.nextFreeSlot[m] = instance.numJobs # indicate that all tasks have been initialized for machine m
		else:
			logging.error("Unknown instance type")
			exit()

	def _start_time(self,t):
		return self.instance.startTime(t.job, t.task)

	def toschedule(self):
		# indicate for each task that have been scheduled, its start time
        startTime = [None]*(self.instance.numTasks) # or 0

        startTimes = [startTime for _ in range(self.instance.numJobs)]

        # for each job, how many tasks have been scheduled (0 initially)
        nextToScheduleByJob = [0]*self.instance.numJobs

        # for each machine, how many tasks have been scheduled (0 initially)
        nextToScheduleByMachine = [0]*self.instance.numMachines

        # for each machine, earliest time at which the machine can be used
        releaseTimeOfMachine = [0]*self.instance.numMachines
        UnscheduledTaskExists = True

        while UnscheduledTaskExists:
        	schedulable = None
        	for m in range(self.instance.numMachines):
        		if nextToScheduleByJob[m] < self.instance.numJobs:
        			for mtask in self.taskByMachine[m]:
        				if mtask.task == nextToScheduleByJob[task.job]:
        					schedulable = mtask
        					break

        	if schedulable is not None:
        		# we found a schedulable task, lets call it t
        		t = schedulable
        		machine = self.instance.machine(t.job, t.task)

        		#compute the earliest start time (est) of the task
        		est = t.task == 0?0 : startTimes[t.job][t.task-1] + self.instance.duration(t.job, t.task-1)
        		est = math.max(est, releaseTimeOfMachine[self.instance.machine(t)])
        		startTimes[t.job][t.task] = est

        		# mark the task as scheduled
                nextToScheduleByJob[t.job]+=1
                nextToScheduleByMachine[machine]+=1
                # increase the release time of the machine
                releaseTimeOfMachine[machine] = est + self.instance.duration(t.job, t.task)
            else:
            	# no tasks are schedulable, there is no solution for this resource ordering
                return None

        # we exited the loop : all tasks have been scheduled successfully
        return Schedule(instance, startTimes)

	def copy(self):
		return copy.deepcopy(self.toschedule)

	def __str__(self):
		s=""
		for m in range(self.instance.numMachines):
			s += "Machine" + m + ":"
			tasks_str=";"
			tasks_str.join(self.taskByMachine[m]) #join tasks or machine m
			s += tasks_str + "\n"
		return s 





