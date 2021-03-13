from sortedcollections import SortedDict
from jobshop.encodings.ResourceOrder import ResourceOrder


class AlgoGloutonSPT():

    def __init__(self, ResOrderObject:ResourceOrder):
        self.resource_order = ResOrderObject

    def __getWaitingOperationsSPT(self, aJobsList, time):
        """Get waiting jobs at current time in shortest duration order"""

        incomingOperations = {}
        assignedJobsForMachine = []
        aJobsList = [job for job in self.resource_order.instance.numJobs
        global machinesList
        for mach in machinesList:
            assignedJobsForMachine = [job for job in aJobsList if job.completed == False and job.machine == mach.name]
            incomingOperations[mach.name] = []

            for j in assignedJobsForMachine:
                if j.idOperation == 1:
                    incomingOperations[mach.name].append(j)
                else:
                    previousTask = [job for job in aJobsList if
                                    job.itinerary == j.itinerary and job.idOperation == j.idOperation - 1 and job.endTime <= time]
                    if len(previousTask):
                        if previousTask[0].completed:
                            incomingOperations[mach.name].append(j)
            # sort added jobs by duration
            incomingOperations[mach.name].sort(key=lambda j: j.duration)
        return incomingOperations

    def runSPT(self):
        """
        SPT/SJF heuristic algorithm for job shop problem
        """
        aJobsList = self.ResourceOrderObject.instance.numJobs

        time = {}
        waitingOperations = {}
        currentTimeOnMachines = {}
        jobsListToExport = []

        # initialize machines times and get
        # first waiting operations for each machine
        global machinesList
        for machine in machinesList:
            waitingOperations[machine.name] = [job for job in aJobsList if
                                               job.machine == machine.name and job.idOperation == 1]
            waitingOperations[machine.name].sort(key=lambda j: j.duration)
            currentTimeOnMachines[machine.name] = 0

        time[0] = waitingOperations

        for keyMach, operations in waitingOperations.items():
            # for each waiting task in front of machine set time to 0, update
            # properties
            if len(operations):
                operations[0].startTime = 0
                operations[0].completed = True

                # push task to production, and create new event to stop at,
                # on ending time, then update machines time
                jobsListToExport.append(operations[0])
                currentTimeOnMachines[keyMach] = operations[0].getEndTime()
                time[currentTimeOnMachines[keyMach]] = {}

        while len(jobsListToExport) != len(aJobsList):
            for t, operations in time.items():
                operations = self.__getWaitingOperationsSPT(aJobsList, float(t))

                for keyMach, tasks in operations.items():
                    if len(tasks):
                        if float(t) < currentTimeOnMachines[tasks[0].machine]:
                            continue

                        tasks[0].startTime = float(t)
                        tasks[0].completed = True

                        jobsListToExport.append(tasks[0])

                        currentTimeOnMachines[keyMach] = tasks[0].getEndTime()
                        time[currentTimeOnMachines[keyMach]] = {}

                del time[t]
                break

            time = SortedDict(time)  # chronological order

        return jobsListToExport
