_B=False
_A=None
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.conf import settings
from django_app.settings import logger,_print,WEBSCRAPER_THREADS_MAX,WEBSCRAPER_TASK_MAX_ATTEMPTS,WEBSCRAPER_THREAD_TIMEOUT
from webscraping.modules.threader.classes.StoppableThread import StoppableThread
from webscraping.modules.threader.classes.TaskProgress import TaskProgress,Status
import threading
from time import sleep
from typing import Union
from datetime import datetime,timedelta
import uuid,copy,json
from uuid import uuid1
from enum import Enum
DEBUG=settings.DEBUG
class TaskHandler:
	'\n        A class to handle background tasks using threading and Django cache.\n        Tasks are tracked and can be stopped gracefully.\n\n        -----------\n        Src:\n            "A simple approach for background task in Django"\n            Handle long running task using Threading and Django Cache\n            - https://ivanyu2021.hashnode.dev/a-simple-approach-for-background-task-in-django\n\n        Update:\n            Mon 03 Feb 2025 w @Deepseek:\n            - Added thread tracking and graceful stopping mechanism using StoppableThread.\n\n\n        Example usage:\n            ```python\n\n                # Long running method\n                def webscrape_steps_long_running_method(webscrape: Webscrape, taskProgress):\n                    def _print(key, value):\n                        print(f\'-------| webscrape_steps_long_running_method > {key}\', value)\n\n                    progress_value = 0\n                    taskProgress.set_unset(\n                        Status.STARTED, progress_value,\n                        progress_message=f\'The webscrape "{webscrape}" has been started\'\n                    )\n\n                    # Example: Execute web scraping steps\n                    for step in webscrape.steps:\n                        # Simulate step execution\n                        progress_value += 10\n                        taskProgress.set_unset(\n                            Status.RUNNING, progress_value,\n                            progress_message=f\'Step {step} has been processed\'\n                        )\n\n                    # Mark task as completed\n                    taskProgress.set_unset(\n                        Status.SUCCESS, 100,\n                        progress_message=f"Webscrape completed successfully"\n                    )\n\n\n                # Example usage\n                task_handler = TaskHandler()\n                webscrape = Webscrape.objects.get(id=1)  # Replace with your model instance\n                task_handler.queue_task(webscrape_steps_long_running_method, [webscrape])\n                task_handler.start_next_tasks()\n            ```\n    ';tasks_running:dict={};tasks_queue:list=[];taskClass=_A
	def __init__(A,taskClass):A.tasks_running={};A.taskClass=taskClass
	@staticmethod
	def get_self_cache_key():"\n            Gets the task handers' cache key, used to retrived and use\n            the object or set it in cache\n\n            Returns:\n                str: the cache key string\n        ";return settings.WEBSCRAPER_TASKHANDLER_CACHE_KEY
	@staticmethod
	def get_taskHandler(taskClass):
		'\n            Gets the current task hander from cache, or instantiates\n            a new one and set it in cache.\n\n            Returns:\n                TaskHandler: the cache key string\n        ';B=TaskHandler.get_self_cache_key();A=cache.get(B)
		if not A:A=TaskHandler(taskClass);cache.set(B,A)
		return A
	@staticmethod
	def get_taskProgress(task_run_id):'\n            Retrieve the TaskProgress object for a given task_run_id.\n\n            Args:\n                task_run_id (str): The ID of the task to retrieve.\n\n            Returns:\n                TaskProgress: The TaskProgress object associated with the task_run_id.\n        ';return cache.get(task_run_id)
	@staticmethod
	def task_is_timedout(task):A=(datetime.now()-task.task_thread_started_at).seconds//60;return A>WEBSCRAPER_THREAD_TIMEOUT
	@staticmethod
	def task_is_queueable(task):
		B=task;A=B.task_status not in(Status.QUEUED.value,Status.RUNNING.value,Status.SUCCESS.value)
		if A:A=B.task_progress<100
		if A:A=B.task_attempts<WEBSCRAPER_TASK_MAX_ATTEMPTS
		if A:
			A=True if not TaskHandler.get_taskProgress(B.task_run_id)else _B
			if not A:A=TaskHandler.task_is_timedout(B)
		return A
	def queue_task(D,method,args,force_run=_B):
		"\n            Add a task to the queue for later execution.\n\n            Args:\n                method (callable): The method to execute in the background.\n                args (list): Arguments to pass to the method. The first element must be a model\n                            with a 'task_run_id' attribute to track the task.\n\n            \n        ";F=force_run;A=args;B=method;E=_B
		for(G,H)in D.tasks_queue:
			if G==B and H[0].id==A[0].id:E=True;break
		if not E:D.tasks_queue.append((B,A))
		if not F:D.start_next_tasks();C=f"Taskhandler.queue_task - QUEUED :: previously? {E} /// {B} - {A}";_print(C,VERBOSITY=0);logger.debug(C);return Status.QUEUED
		if F:D.start_task(B,A);C=f"Taskhandler.queue_task - RUNNING ::  /// {B} - {A}";_print(C,VERBOSITY=0);logger.debug(C);return Status.RUNNING
	def start_task(B,method,args,taskObject=_A):
		"\n            Start a new background task in a separate thread.\n\n            Args:\n                method (callable): The method to execute in the background.\n                args (list): Arguments to pass to the method. The first element must be a model\n                            with a 'task_run_id' attribute to track the task.\n                taskObject (ThreadTask) (optional):\n                            The ThreadClass model or subclass of, instance to for which to start a thread\n\n            Returns:\n                str: The task_run_id of the newly started task.\n        ";A=taskObject;E=TaskProgress(B);C=E.get_task_run_id();D=StoppableThread(target=method,args=[*args,E]);D.setDaemon(True);D.start();B.tasks_running[C]=D
		try:
			if not A:A=B.taskClass.objects.get(task_run_id=C)
			if not A.task_attempts:A.task_attempts=0
			A.task_attempts=A.task_attempts+1;A.task_status=Status.RUNNING.value;A.task_thread_started_at=datetime.now();A.save()
		except Exception as F:logger.error(f"{datetime.now()} - Taskhandler.start_task - taskObject.save() ERROR : {F}")
		logger.debug('Taskhandler.start_task - RUNNING > len(self.tasks_running.keys()) > : %i'%len(B.tasks_running.keys()));return C
	def start_next_tasks(A,forceStartTaskObjects=[]):
		'\n            Start the next task in the queue if any tasks are waiting.\n\n            Return\n                (int, int): number of tasks started, number of tasks runnning\n        ';B=[f"Taskhandler.start_next_tasks - WEBSCRAPER_THREADS_MAX :: {WEBSCRAPER_THREADS_MAX}"];B.append(f"Taskhandler.start_next_tasks - QUEUED TASKS :: {len(A.tasks_queue)}");B.append(f"Taskhandler.start_next_tasks - RUNNING TASKS :: {len(A.tasks_running.keys())}")
		for D in B:logger.debug(D),print(D)
		E=0
		while len(A.tasks_running.keys())<=WEBSCRAPER_THREADS_MAX:
			if len(A.tasks_queue):
				F,C=A.tasks_queue.pop(0);G=C[0]
				if G.task_attempts<WEBSCRAPER_TASK_MAX_ATTEMPTS:A.start_task(F,C,taskObject=G);logger.debug('Taskhandler.start_next_tasks - obj SAVED > : %s - %s'%(str(F),str(C)));E+=1
		return E,len(A.tasks_running.keys())
	def end_task(A,task_run_id,taskObject=_A,do_save=_B):
		'\n            Ends a running task and flush it from memory.\n\n            Args:\n                task_run_id (str): The ID of the task to terminate.\n                taskObject (ThreadTask) (optional):\n                            The ThreadClass model or subclass of, instance to for which to start a thread\n                do_save (book) (optional):\n                            if database save should be done here, or not\n        ';D=task_run_id;B=taskObject;A.start_next_tasks()
		try:
			if not B:B=A.taskClass.objects.get(task_run_id=D)
		except Exception as F:E='Taskhandler.end_task - Exception : %s '%str(F);_print(E,VERBOSITY=0),logger.debug(E)
		if D in A.tasks_running:
			C=A.tasks_running[D]
			if DEBUG:logger.debug('Taskhandler.start_next_tasks - thread IS_ALIVE > %s '%str(C.is_alive()))
			if C and C.is_alive():
				try:
					C.stop()
					if C!=threading.current_thread():C.join()
					else:logger.debug('Cannot join current thread, skipping join')
				except RuntimeError as F:E='Taskhandler.end_task - RuntimeError : %s '%str(F);_print(E,VERBOSITY=0),logger.debug(E)
			A.tasks_running[D]=_A;del A.tasks_running[D]
			if B:
				B.task_thread_stopped_at=datetime.now()
				if do_save:B.save()
			return B
	def end_task_start_next(B,task_run_id,taskObject=_A,do_save=_B):'\n            Calls end_task to ends a running task and flush it from memory.\n            Starts the next one in queue, if existing...\n\n            Args:\n                task_run_id (str): The ID of the task to terminate.\n                taskObject (ThreadTask) (optional):\n                            The ThreadClass model or subclass of, instance to for which to start a thread\n                do_save (book) (optional):\n                            if database save should be done here, or not\n\n            Return\n                (ThreadTask,    ThreadTask model instance or subclass of\n                                for which the thread has been started\n                    int, int):  number of tasks started, number of tasks runnning\n        ';A=taskObject;A=B.end_task(task_run_id,taskObject=A,do_save=do_save);C,D=B.start_next_tasks();return A,C,D