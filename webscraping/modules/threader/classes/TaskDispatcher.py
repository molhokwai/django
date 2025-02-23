_C='QUEUED'
_B='SUCCESS'
_A=None
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.conf import settings
from django_app.settings import logger,_print,WEBSCRAPER_TASK_MAX_ATTEMPTS,WEBSCRAPER_THREAD_TIMEOUT,WEBSCRAPER_THREAD_TIMEOUT_FROM_CREATION
from webscraping.models import ThreadTask,Webscrape
from webscraping.modules.threader.classes.TaskHandler import TaskHandler
from webscraping.modules.threader.classes.TaskProgress import Status
from webscraping.views import webscrape_steps_long_running_method
import threading
from time import sleep
from typing import Union
from datetime import datetime,timedelta
import uuid,copy,json
from uuid import uuid1
from enum import Enum
DEBUG=settings.DEBUG
class TaskDispatcher:
	'\n        A class to check and dispatch tasks...\n\n        Example usage:\n            ```python\n\n                # Example usage\n                task_dispatcher = TaskDispatcher()\n                ...\n            ```\n    ';taskClass:ThreadTask=_A
	def __init__(A,taskClass):A.taskClass=taskClass
	_taskHandler=_A
	@property
	def taskHandler(self):
		A=self
		if not A._taskHandler:A._taskHandler=TaskHandler.get_taskHandler(A.taskClass)
		return A._taskHandler
	def check_tasks_to_queue(C,timeout=_A):
		'\n            Querying, then filtering tasks for tasks to run\n            Then dispatching them...\n\n            1. Check that status is not QUEUED, RUNNING  or SUCCESS\n            2. Check that progress is not 100%\n            3. Check that MAX_ATTEMPTS is not reached\n            4. \n                if 1, 2, 3: check that task does not have TaskProgress, or that \n                Task thread timeout is reached: \n                  datetime.now – task_thread_started_at >= TASK_TIMEOUT\n\n            Return:\n                Dispacthed tasks: Union[List, None]\n        ';D=timeout;F=D or WEBSCRAPER_THREAD_TIMEOUT;G=D or WEBSCRAPER_THREAD_TIMEOUT_FROM_CREATION;H=~Q(task_status__in=[_C,'RUNNING',_B])&Q(task_progress__lt=100)&Q(task_attempts__lt=settings.WEBSCRAPER_TASK_MAX_ATTEMPTS);I=~Q(task_status__in=[_C,_B])&Q(task_progress__lt=100)&Q(task_attempts__lt=settings.WEBSCRAPER_TASK_MAX_ATTEMPTS)&(Q(task_thread_started_at__lt=datetime.now()-F)|Q(created_on__lt=datetime.now()-G));A=C.taskClass.objects.filter(H|I)
		if len(A):
			for B in A:J=C.dispatch(B.task_todo,B);B.task_status=J.value;B.save()
		E=f"""

\t\t--------------------------------------------------------
\t\tTASKS TO QUEUE: checking and dispatching completed: {len(A)} tasks done.
\t\t--------------------------------------------------------

""";print(E),logger.info(E);return A
	def dequeue_and_run(C):
		'\n            Querying, then filtering tasks for tasks to run\n            Then dispatching them...\n\n            1. Check that status is not QUEUED, RUNNING  or SUCCESS\n            2. Check that progress is not 100%\n            3. Check that MAX_ATTEMPTS is not reached\n            4. \n                if 1, 2, 3: check that task does not have TaskProgress, or that \n                Task thread timeout is reached: \n                  datetime.now – task_thread_started_at >= TASK_TIMEOUT\n\n            Return:\n                Dispacthed tasks: Union[List, None]\n        ';E=Q(task_status__in=[_C])&Q(task_progress__lt=100)&Q(task_attempts__lt=settings.WEBSCRAPER_TASK_MAX_ATTEMPTS);A=C.taskClass.objects.filter(E)
		if len(A):
			for B in A:F=C.dispatch(B.task_todo,B);B.task_status=F.value;B.save()
		D=f"""

\t\t--------------------------------------------------------
\t\tTASKS TO DEQUEUE AND RUN: checking and dispatching completed: {len(A)} tasks done.
\t\t--------------------------------------------------------

""";print(D),logger.info(D);return A
	def check_tasks_to_end(E,_which,webscrapes=_A,status=_A,timeout=_A):
		'\n            For each task with status=(arg:None)\n            + for each task in running queue:\n            ________________________________\n\n\n            1. Check if task is completed, or if task has reached timeout:\n               - if completed: set task status SUCCESS\n               - if timed out: set task status FAILED\n               - call `taskHandler.end_task_start_nexts`\n\n            2. if not completed and not timed out:\n               - Do nothin, pass\n        ';F='task_is_timedout_Q';G='task_is_completed_Q';H=timeout;I=status;B=_which;R=H or WEBSCRAPER_THREAD_TIMEOUT;S=H or WEBSCRAPER_THREAD_TIMEOUT_FROM_CREATION;J={G:(~Q(task_status=_B)&Q(task_progress__gte=100),Status.SUCCESS.value),F:(~Q(task_status=_B)&(Q(task_thread_started_at__lt=datetime.now()-R)|Q(created_on__lt=datetime.now()-S)),Status.FAILED.value)};C=[];K=0;L=0;M,N=0,0
		for D in J:
			O=J[D];T=O[0];I=O[1];U=E.taskClass.objects.filter(T)
			for A in U:
				if B=='update':A.task_status=I;A.save()
				elif B=='end':A,V,W=E.taskHandler.end_task_start_next(A.task_run_id,taskObject=A);M+=V;N+=W
				if D==G:K+=1
				elif D==F:L+=1
				C.append(A)
		P=f"""

\t\t--------------------------------------------------------
\t\tTASKS TO {B.upper()}: checking completed::
\t\t- {K} tasks completed
\t\t- {L} tasks timed out
\t\t- {len(C)} tasks ended, {M} started, {N} running...
\t\t--------------------------------------------------------

""";print(P),logger.info(P);return C
	def dispatch(B,task_name,webscrape,force_run=False):'\n        Dispatches tasks based on the task_name.\n\n        Args:\n            task_name (str): The name of the task to execute.\n            webscrape (Webscrape): The Webscrape instance associated with the task.\n        ';A=task_name;C={'webscrape_steps_long_running_method':webscrape_steps_long_running_method}.get(A,ValueError(f"Unknown task: {A}"));D=B.taskHandler.queue_task(C,[webscrape],force_run=force_run);return D