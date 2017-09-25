#!/usr/bin/python

import dbm
import json
import datetime
import argparse
import string

class MyEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__

#json.dumps(cls=MyEncoder)

class WorkEntry:
	entry_id = 0
	comment = ""
	duration = 0
	task_id	= 0
	when = datetime.datetime.now()

	def __init__(self):
		pass
	def __init__(self, task_id=-1, comment=None, duration=-1,js=None):
		self.when = datetime.datetime.now()

		self.entry_id = -1
		self.task_id = task_id
		self.comment = comment
		self.duration = duration

		if js!=None:
			self.__dict__ = json.loads(js)

	def get_json(self):
		json_dict = self.__dict__.copy()
		json_dict['when'] = self.when.strftime("YYYY-MM-DD HH:mm")
		return json.dumps(json_dict)

	list_template = string.Template("""
$when :: $entry_id/$task_id
	$duration
	$comment 
""")

	def list_str(self):
		return self.list_template.substitute(self.__dict__)


class Task:
	task_id = 0
	version = 0
	name = ""
	description = ""
	estimate = 0
	job_number = 43146
	is_open = True

	def __init__(self):
		pass
	def __init__(self, job_number=-1, name=None, description=None, estimate=-1, js=None):

		self.version = 0
		self.task_id=-1
		self.name = name
		self.description = description
		self.job_number = job_number
		self.estimate = estimate
		self.is_open = True

		if js != None:
			self.__dict__ = json.loads(js)
	def get_json(self):
		return json.dumps(self.__dict__)

	detail_template = string.Template("""
============================
$task_id - $name v:$version 
job: $job_number
----------------------------
$description
----------------------------
Estimate: $estimate
Time Logged: $time_logged

""")
	list_template = string.Template("""$task_id/$version::$job_number\t\t$name\t\t$estimate""")

	def list_header():
		return Task.list_template.substitute({
			'task_id':'id',
			'version':'version',
			'name':'task name',
			'job_number':'job_#',
			'estimate':'estimate'})

	def list_str(self):
		return self.list_template.substitute(self.__dict__)

	def detail_str(self, time_logged):
		display_copy = self.__dict__.copy()
		display_copy["time_logged"] = time_logged
		return self.detail_template.substitute(display_copy)

class Dao:
	db = None

	def __init__(self, db):
		self.db = db

	def get_log(self, log_id):
		log_item_json = self.db.get("log.{}".format(log_id), None)
		if log_item_json != None:
			log_item = WorkEntry(js=log_item_json)
			return log_item
		return None

	def get_task_log(self, task_id):
		log_list_json = self.db.get("t.{}.log".format(task_id), "[]")
		log_list = json.loads(log_list_json)
		logs = []

		for log_id in log_list:
			log_json = self.db.get("log.{}".format(log_id), None)
			log_item = None
			if log_json != None:
				log_item = WorkEntry(js=log_json)
				logs.append(log_item)
		return logs


	def get_task(self, task_id, version=-1):
		task = None
		if version < 0:
			version = int(self.db.get("t.{}.latest".format(task_id), 0))
		task_json = self.db.get("t.{}.{}".format(task_id, version), None)
		if task_json != None:
			task = Task(js=task_json)
		return task

	def get_tasks(self):
		id_list_json = self.db.get("tasks", "[]")
		id_list = json.loads(id_list_json)
		tasks = []
		for task_id in id_list:
			version = int(self.db.get("t.{}.latest".format(task_id), 0))
			task_json = self.db.get("t.{}.{}".format(task_id, version), None)
			task = None
			if task_json != None:
				task = Task(js=task_json)
				tasks.append(task)
		return tasks


	def store_log(self, log_item):
		entry_id = int(self.db.get("last_log_id", -1))
		if log_item.entry_id < 0:
			log_item.entry_id = entry_id + 1
			self.db["last_log_id"] = str(log_item.entry_id)

		self.db["log.{}".format(log_item.entry_id)]=log_item.get_json()

		log_list_json = self.db.get("t.{}.log".format(log_item.task_id), "[]")
		log_list = json.loads(log_list_json)
		if not log_item.entry_id in log_list:
			log_list.append(log_item.entry_id)
			self.db["t.{}.log".format(log_item.task_id)] = json.dumps(log_list)

		
	def store_task(self, task):
		task_id = int(self.db.get("last_task_id", -1))
		if task.task_id < 0:
			task.task_id = task_id + 1
			self.db["last_task_id"] = str(task.task_id)
		id_list_json = self.db.get("tasks", "[]")
		id_list = json.loads(id_list_json)
		self.db["t.{}.latest".format(task.task_id)]=str(task.version)
		self.db["t.{}.{}".format(task.task_id, task.version)]=task.get_json()
		if not task.task_id in id_list:
			id_list.append(task.task_id)
			self.db["tasks"]=json.dumps(id_list)


def _list_tasks(dao, open_only=True):
	tasks = []
	if open_only:
		tasks = [task for task in dao.get_tasks() if task.is_open == True]
	else:
		tasks = dao.get_tasks()
	for task in tasks:
		print(task.list_str())

def list_tasks(dao, arguments):
	open_only = True
	if arguments.open_only:
		open_only=not arguments.open_only
	print(Task.list_header())
	print('-'*72)
	_list_tasks(dao,open_only)
	
def report_all(dao, task_id):
	logs = dao.get_task_log(task_id)
	for item in logs:
		print(item.list_str())

def _report(dao, task_id, since):
	logs = dao.get_task_log(task_id)
	logs_since = [ item for item in logs if item.when > since]
	for item in logs_since:
		print(item.list_str())

def report(dao, arguments):
	_report(dao, arguments.task_id, arguments.since)

def _view_task(dao, task_id):
	task = dao.get_task(task_id)
	if task != None:
		logs = dao.get_task_log(task_id)
		time_logged = 0
		for log in logs:
			time_logged += log.duration
		print(task.detail_str(time_logged))
	else:
		print("No such task")
def view_task(dao, arguments):
	_view_task(dao, arguments.task_id)

def _new_log(dao, task_id, comment, duration):
	log_item = WorkEntry(task_id,comment,duration)
	dao.store_log(log_item)
	print("Saved Log Item...")
	print(dao.get_log(log_item.entry_id).list_str())

def new_log(dao, arguments):
	_new_log(dao, arguments.task_id, arguments.comment,arguments.duration)

def _new_task(dao, job_number, name, description, estimate):
	task = Task(job_number, name, description, estimate)
	dao.store_task(task)
	print("Saved Task...")
	_view_task(dao, task.task_id)

def new_task(dao, arguments):
	_new_task(dao, arguments.job_number,arguments.name,arguments.description,arguments.estimate)

def _update_task(dao, task_id, job_number=-1, name=None, description=None, estimate=-1):
	task = dao.get_task(task_id)
	if task != None:
		task.version +=1
		if job_number > 0:
			task.job_number = job_number
		if name != None:
			task.name = name
		if description != None:
			task.description = description
		if estimate > 0:
			task.estimate = estimate
		dao.store_task(task)
		print("Task successfully updated:")
		task_detail(dao, task_id)
	else:
		print("No such task")

def update_task(dao, arguments):
	job_number = -1
	name = None
	description = None
	estimate = -1

	if arguments.job_number:
		job_number = arguments.job_number
	if arguments.name:
		name = arguments.name
	if arguments.description:
		description = arguments.description
	if arguments.estimate:
		estimate = arguments.estimate

	_update_task(dao, arguments.task_id, job_number, name, description, estimate)

def _update_log(dao, log_id, comment=None, duration=-1):
	log_entry = dao.get_log(log_id)
	if log_entry != None:
		if comment != None:
			log_entry.comment = comment
		if duration >= 0:
			log_entry.duration = duration
		dao.store_log(log_entry)
		print("Saved Log Item...")
		print(dao.get_log(log_id).list_str())
def update_log(dao, arguments):
	comment = None
	duration = -1

	if arguments.comment:
		comment = arguments.comment
	if arguments.duration:
		duration = arguments.duration

	_update_log(dao, arguments.log_id, comment, duration)


command_help="""command to perform against task list
  Options include:
    * list
    * view
    * report
    * log
    * new
    * update
"""


def valid_datetime_type(arg_datetime_str):
    """custom argparse type for user datetime values given from the command line"""
    try:
        return datetime.datetime.strptime(arg_datetime_str, "%Y-%m-%d %H:%M")
    except ValueError:
        msg = "Given Datetime ({0}) not valid! Expected format, 'YYYY-MM-DD HH:mm'!".format(arg_datetime_str)
        raise argparse.ArgumentTypeError(msg)  

if __name__=='__main__':
	with dbm.open('tasks', 'c') as db:
		dao = Dao(db)

		parser = argparse.ArgumentParser(description='Simple Task Tracker')
		parser.set_defaults(func=parser.print_help)
		subparsers = parser.add_subparsers(help='command help')

		list_parser = subparsers.add_parser('list', help='lists tasks')
		list_parser.add_argument('--all',dest='open_only',action='store_true', help='list all open/closed tasks')
		list_parser.set_defaults(func=list_tasks)

		view_parser = subparsers.add_parser('view', help='view a specific task')
		view_parser.add_argument('task_id',type=int, help='id of task to view')
		view_parser.set_defaults(func=view_task)

		report_parser = subparsers.add_parser('report', help='reports on log since a given date')
		report_parser.add_argument('since', type=valid_datetime_type,
			help='start datetime in format "YYYY-MM-DD HH:mm"')
		report_parser.set_defaults(func=report)

#task_id, comment, duration
		log_parser = subparsers.add_parser('log', help='log time against a task')
		log_parser.add_argument('task_id', type=int, help='id of task to log time against')
		log_parser.add_argument('comment', type=str, help='a brief description of the work done')
		log_parser.add_argument('duration', type=float, help='time duration in hours')
		log_parser.set_defaults(func=new_log)

		log_update_parser = subparsers.add_parser('update-log', help='update log entry')
		log_update_parser.add_argument('log_id', type=int, help='id of log item to update')
		log_update_parser.add_argument('comment', type=str, help='a brief description of the work done')
		log_update_parser.add_argument('duration', type=float, help='time duration in hours')
		log_update_parser.set_defaults(func=update_log)

#job_number, name, description, estimate
		task_parser = subparsers.add_parser('new', help='create a new task')
		task_parser.add_argument('job_number', type=int, help='job number task relates to')
		task_parser.add_argument('name', type=str, help='name of this task')
		task_parser.add_argument('description', type=str, help='a brief description of this task')
		task_parser.add_argument('estimate', type=float, help='time estimate in hours')
		task_parser.set_defaults(func=new_task)

		task_update_parser = subparsers.add_parser('update-task', help='update task information')
		task_update_parser.add_argument('task_id', type=int, help='Id of task to update')
		task_update_parser.add_argument('--job_number', type=int, help='job number task relates to')
		task_update_parser.add_argument('--name', type=str, help='name of this task')
		task_update_parser.add_argument('--description', type=str, help='a brief description of this task')
		task_update_parser.add_argument('--estimate', type=float, help='time estimate in hours')
		task_update_parser.set_defaults(func=update_task)

		arguments = parser.parse_args()
		if arguments.func != parser.print_help:
			arguments.func(dao, arguments)
		else:
			parser.print_help()

