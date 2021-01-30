import copy 
from Encoding import *
from Task import *

class ResourceOrder(Encoding):
	def __init__(self):
		super(Encoding, self).__init__()
		self.taskByMachine=[][]
		self.nextFreeSlot=[]
	
	def resourceOrder(self, instance):
		super(Encoding, self).__init__(instance)

	def toschedule(self):
		startTimes = 
		pass

	def copy(self):
		return copy.deepcopy(self.toschedule)

	def __str__():
		s=""
		for m in range(self.instance.numMachines):
			s += "Machine" + m + ":"
			tasks_str=";"
			tasks_str.join(self.taskByMachine[m]) #join tasks or machine m
			s += tasks_str + "\n"
		return s 





