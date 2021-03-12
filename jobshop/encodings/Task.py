

class Task(object):
	"""docstring for Task"""
	def __init__(self, job, task):
		super(Task, self).__init__()
		self.job = job
		self.task= task

	def __eq__(self, other_task):
		return (self.job == otherTask.age) and (self.task == otherTask.task)

	def __hash__(self):
		return hash(self.job, self.task)

	def __str__(self):
		return "(" + str(self.job) +", " + str(self.task) + ')'


		