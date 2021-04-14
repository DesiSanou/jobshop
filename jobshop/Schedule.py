from jobshop.encodings.Task import Task
from jobshop.Instance import Instance
import numpy as np
import copy

class Schedule:

    def __init__(self, pb, times):
        self.pb = pb
        self.times = np.zeros((pb.numJobs, pb.numTasks))
        #self.times = [[] for i in range(pb.numJobs)]

        print("times", times)


        for j in range (pb.numJobs):
            self.times[j] = times[j]
            if len(times[j]) - pb.numTasks > 0:
                self.times[j] = copy.deepcopy(pb.numTasks)




    def startTime(self,  *kwargs):
        if isinstance(kwargs[0], Task):
            return self.startTime(kwargs[0].job, kwargs[0].task)
        else:
            job = kwargs[0]
            task = kwargs[1]
            return self.times[job, task]


    def isValid(self):

        for j in range(self.pb.numJobs):
            for t in range(1,self.pb.numJobs):
                if self.startTime(j, t-1 ) + self.pb.duration(j,t-1) > self.startTime(j, t):
                    return False

            for t in range(1, self.pb.numJobs):
                if self.startTime(j, t) < 0:
                    return False

        for machine in range(self.pb.numMachines):
            for j1 in range(self.pb.numJobs):
                t1 = self.pb.task_with_machine(j1,machine)
                for j2 in range(j1+1, self.pb.numJobs):
                    t2 = self.pb.task_with_machine(j2, machine)

                    t1_first = self.startTime(j1, t1) + self.pb.duration(j1, t1) <= self.startTime(j2, t2);
                    t2_first = self.startTime(j2, t2) + self.pb.duration(j2, t2) <= self.startTime(j1, t1);

                    if t1_first != True and t2_first != True :
                        return False

        return True

    def makespan(self):

        m = -1;
        for j in range(self.pb.numJobs):
            m = max(m, self.startTime(j, self.pb.numTasks -1) + self.pb.duration(j, self.pb.numTasks -1))
        return m



    def endTime(self, Task):
        return self.startTime(Task) + self.pb.duration(Task.job, Task.task)



    def isCriticalPath(self, tasksList):

        if self.startTime(tasksList[0]) != 0:
            return False

        if self.endTime(tasksList[-2]) != self.makespan():
            return  False

        return True

    def criticalPath(self):


        tmp = [Task(j, self.pb.numTasks - 1) for j in range(self.pb.numJobs)]
        ldd = max(sorted(tmp, key=lambda x: self.endTime(x), reverse=True))
        assert self.endTime(ldd) == self.makespan()

        path = []
        path.insert(0, ldd)

        while self.startTime(path[0]) != 0:
            cur = path[0] # cur : Task
            machine = self.pb.machine(cur.job, cur.task)

            latestPredecessor = None

            if cur.task > 0:
                predOnJob = Task(cur.job, cur.task - 1)

                if self.endTime(predOnJob) == self.startTime(cur):
                    latestPredecessor = predOnJob
            if (latestPredecessor is None):
                latestPredecessor = [Task(j, self.pb.task_with_machine(j, machine)) for j in range(self.pb.numJobs)]
                latestPredecessor = list(
                    filter(lambda elem: self.endTime(elem) == self.startTime(cur), latestPredecessor))
                latestPredecessor = latestPredecessor[0]

            assert latestPredecessor is not None and self.endTime(latestPredecessor) == self.startTime(cur)

            path.insert(0, latestPredecessor)
        assert self.isCriticalPath(path)
        return path

if __name__ == '__main__':
    instance = Instance.fromFile("instances/abz5")

    startTimes = np.zeros((instance.numJobs,instance.numTasks))

    schedule = Schedule(instance, startTimes)

    isval = Schedule.isValid(schedule)

    task = Task(1,1)

    mach = instance.duration(1, 1)
    mach1 = instance.duration(task)


    print("abz ", isval)
