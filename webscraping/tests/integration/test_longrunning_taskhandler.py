_A=None
from django.test import SimpleTestCase,TestCase,TransactionTestCase
from webscraping.modules.threader.classes.TaskHandler import TaskHandler
from webscraping.modules.threader.classes.TaskProgress import TaskProgress,Status
from webscraping.models import Webscrape
import re,datetime,time
from typing import Union
class ProcessObject:'\n        processObj = {\n            "title": "A process object with: task_run_id, task_progress, task_outputs",\n            "task_run_id": None,\n            "task_progress": None,\n            "task_outputs": None,\n        }\n    ';task_run_id:Union[str,_A]=_A;task_progress:Union[int,_A]=_A;task_status:Union[str,_A]=_A;task_outputs:Union[list,_A]=_A;description:str='A process object with: task_run_id, task_progress, task_outputs'
class LongRunningTaskHandlerTestCases(TransactionTestCase):
	'\n        -----------\n        @T :: SimpleTestCase →to TestCase →to TransactionTestCase\n        @T ::   try:\n                    ...\n                except django.db.utils.OperationalError as err:\n                    ...\n\n        @T ::   darklight.Blog.date_created: (fields.W161) Fixed default value provided.\n                HINT: It seems you set a fixed date / time / datetime value as default for this field. This may not be what you want. If you want to have the current date as default, use `django.utils.timezone.now`\n\n        @T ::   Status.STATUS instead of Status.SUCCESS\n\n                :167    taskProgress.set_unset(\n                            Status.STATUS, progress_value,\n                            progress_message=f"{output}% has been processed" )\n\n\n\n        -----------\n        Src:\n            "A simple approach for background task in Django"\n            Handle long running task using Threading and Django Cache\n            - https://ivanyu2021.hashnode.dev/a-simple-approach-for-background-task-in-django\n    '
	def from_source(A):0
	@staticmethod
	def _print(key,value):print(f"webscraping.tests.integration.test_long_running_task - {key} :: {value}")
	def test_long_running_task(D):
		B=LongRunningTaskHandlerTestCases._print;C=ProcessObject();C.task_run_id=TaskHandler().start_task(D.long_running_method,[C]);E=re.compile('[a-f0-9]{8}-[a-f0-9]{4}-1[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$',re.IGNORECASE);D.assertEqual(E.match(C.task_run_id)is not _A,True);B('processObj.task_run_id',C.task_run_id);F=0;A=TaskHandler.get_taskProgress(C.task_run_id)
		while A.status!=Status.SUCCESS:
			try:
				time.sleep(1);A=TaskHandler.get_taskProgress(C.task_run_id);H=A.value;D.assertTrue(A.value is not _A);B('taskProgress.value',A.value);B('taskProgress.status',A.status)
				if A.status==Status.SUCCESS:B(f"{A.status} > output",A.output);break
				B(f"{A.status} > progress_message",A.progress_message);F+=1
			except OperationalError as G:B('Caught <django.db.utils.OperationalError>: ',G)
		D.assertTrue(A.outputs is not _A);B('test_long_running_task > taskProgress.outputs',A.outputs);B('test_long_running_task > processObj.task_outputs',C.task_outputs)
	def long_running_method(K,processObj,taskProgress):
		C=taskProgress;B=processObj;D=LongRunningTaskHandlerTestCases._print;A=0;C.set_unset(Status.STARTED,A,progress_message=f'The process with object "{B}" has been started');G=range(2);E=len(G)
		for H in range(E):
			for I in range(10):
				time.sleep(1);F=5*I+1;A=int(H/E*100)
				if A>=100:A=100
				C.set_unset(Status.RUNNING if A<100 else Status.SUCCESS,A,progress_message=f"{F}% has been processed",output=F);B.task_progress=A;B.task_status=C.status;B.task_outputs=C.outputs
				if A>=100 or C.status==Status.SUCCESS:break
		J=f"[{datetime.datetime.now()}] input::{B}, outputs::{C.outputs}";A=100;C.set_unset(Status.SUCCESS,A,progress_message=f"{J}% have been processed");B.task_progress=A;B.task_status=C.status;D('long_running_method > taskProgress.status',C.status);D('long_running_method > processObj.task_progress',B.task_progress);D('long_running_method > processObj.task_outputs',B.task_outputs)