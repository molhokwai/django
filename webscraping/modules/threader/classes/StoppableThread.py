_A=None
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django_app.settings import logger,WEBSCRAPER_THREAD_TIMEOUT
import threading
from time import sleep
from typing import Union
from datetime import datetime,timedelta
DEBUG=settings.DEBUG
class StoppableThread(threading.Thread):
	'\n        A thread that can be stopped gracefully using a flag.\n    ';task_run_id:Union[str,_A]=_A
	def __init__(A,timeout=settings.WEBSCRAPER_THREAD_TIMEOUT,*D,**B):
		C='args'
		if C in B and len(B[C])>1:E=B[C][1];A.task_run_id=E.get_task_run_id()
		else:raise ValueError("Missing or invalid 'args' in kwargs")
		super().__init__(*D,**B);A._stop_event=threading.Event();A.timeout=timeout;A.start_time=_A
	def stop(A):'\n        Signal the thread to stop.\n        ';print("Thread with task_run_id '%s': STOP..."%A.task_run_id);A._stop_event.set()
	def stopped(A):
		'\n        Check if the thread has been signaled to stop.\n        ';B=A._stop_event.is_set()
		if B:print("Thread with task_run_id '%s' is STOPPING..."%A.task_run_id)
		return A._stop_event.is_set()
	def run(A):
		'\n        Override the run method to periodically check the stop flag.\n        '
		try:
			super().run()
			if A.start_time is _A:A.start_time=datetime.now()
			while not A.stopped():
				B=datetime.now();logger.debug("StoppableThread.run with task_run_id '%s' - NOW / START_TIME : %s / %s"%(A.task_run_id,B,A.start_time))
				if B-A.start_time>A.timeout:logger.debug("Thread with task_run_id '%s' stopping due to timeout..."%A.task_run_id);print(f"Thread w task_run_id '{A.task_run_id}' stopping due to timeout...");A.stop();break
				else:print("Thread with task_run_id '%s' is RUNNING..."%A.task_run_id);sleep(5)
			print('Thread stopped gracefully.')
		except Exception as D:C=f"Error in thread {A.task_run_id}: {D}";logger.debug(C);logger.error(C);A.stop();print('Thread stopped gracefully due to an error.')