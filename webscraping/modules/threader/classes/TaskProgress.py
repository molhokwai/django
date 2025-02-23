_A=None
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from django.conf import settings
from django_app.settings import logger,_print,WEBSCRAPER_CACHING_DURATION
import threading
from time import sleep
from typing import Union
from datetime import datetime,timedelta
import uuid,copy,json
from uuid import uuid1
from enum import Enum
DEBUG=settings.DEBUG
class Status(Enum):'\n        Enum representing the possible statuses of a task.\n    ';RUNNING='RUNNING';QUEUED='QUEUED';SUCCESS='SUCCESS';FAILED='FAILED';STARTED='STARTED'
class TaskProgress:
	'\n        A class to track the progress of a background task.\n\n        -----------\n        Src:\n            "A simple approach for background task in Django"\n            Handle long running task using Threading and Django Cache\n            - https://ivanyu2021.hashnode.dev/a-simple-approach-for-background-task-in-django\n    ';task_run_id:Union[str,_A]=_A;status:Status=Status.RUNNING;value:Union[int,_A]=_A;output:Union[int,_A]=_A;taskHandler=_A
	def __init__(A,taskHandler):A.task_run_id=str(uuid1());cache.set(A.task_run_id,A,3600);A.taskHandler=taskHandler
	def set_unset(A,status,value,progress_message=_A,expires_in=_A,_print_progress=True):
		"\n        Update the task's status and progress, and manage its cache lifecycle.\n\n        Args:\n            status (Status): The new status of the task.\n            value (int): The progress value (e.g., percentage).\n            progress_message (str, optional): A message describing the progress.\n            expires_in (int, optional): The cache expiration time in seconds.\n            _print (bool, optional): Print progress message.\n\n        Returns:\n            object: The updated TaskProgress object.\n        ";C=status;B=expires_in;A.status=C;A.value=value;A.progress_message=progress_message
		if C.value in[Status.SUCCESS.value,Status.FAILED.value]:A.taskHandler.end_task_start_next(A.task_run_id);cache.delete(A.task_run_id)
		elif cache.get(A.task_run_id):
			if B:cache.set(A.task_run_id,A,B)
		else:cache.set(A.task_run_id,A,B or settings.WEBSCRAPER_CACHING_DURATION)
		if _print_progress:_print(A.progress_message)
	def get_task_run_id(A):'\n        Get the task_run_id of this task.\n\n        Returns:\n            str: The task_run_id.\n        ';return A.task_run_id
	def __str__(A):return f"{A.task_run_id} - {A.status} {A.value} {A.outputs}"