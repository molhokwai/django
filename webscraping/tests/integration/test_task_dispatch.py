_F='localhost-test.sequences/localhost-test.sequence.json'
_E='localhost'
_D='task_name'
_C='country'
_B='website_url'
_A=None
from django.test import SimpleTestCase,TestCase,TransactionTestCase
from django.db.utils import OperationalError
from webscraping.modules.threader.classes.TaskDispatcher import TaskDispatcher
from webscraping.modules.threader.classes.TaskProgress import Status
from webscraping.models import Webscrape
import re,datetime,time
from typing import Union
class ProcessObject:'\n        processObj = {\n            "title": "A process object with: task_run_id, task_progress, task_outputs",\n            "task_run_id": None,\n            "task_progress": None,\n            "task_outputs": None,\n        }\n    ';task_run_id:Union[str,_A]=_A;task_progress:Union[int,_A]=_A;task_status:Union[str,_A]=_A;task_outputs:Union[list,_A]=_A;description:str='A process object with: task_run_id, task_progress, task_outputs'
class TasksDispatchTestCases(TransactionTestCase):
	@staticmethod
	def _print(key,value):print(f"webscraping.tests.integration.test_long_running_task - {key} :: {value}")
	def test_queue_task(B):C={_B:_E,_C:'US',_D:_F};A=Webscrape(**C);A.task_variables=model_to_dict(B.webscrape);A.save();assertTrue(A.id>0);assertTrue(A.task_progress<100);assertTrue(A.task_status!=Status.SUCCESS);D=TaskDispatcher(Webscrape);D.dispatch(A.task_name,A);sleep(30);assertTrue(A.task_progress>=100);assertTrue(A.task_status==Status.SUCCESS)
	def test_queue_task_force_run(B):C={_B:_E,_C:'US',_D:_F};A=Webscrape(**C);A.task_variables=model_to_dict(B.webscrape);A.save();assertTrue(A.id>0);assertTrue(A.task_progress<100);assertTrue(A.task_status!=Status.SUCCESS);D=TaskDispatcher(Webscrape);D.dispatch(A.task_name,A,force_run=True);sleep(30);assertTrue(A.task_progress>=100);assertTrue(A.task_status==Status.SUCCESS)
	def test_faling_task(B):C={_B:_E,_C:'US',_D:'localhost-test.sequences/localhost-test-fail.sequence.json'};A=Webscrape(**C);A.task_variables=model_to_dict(B.webscrape);A.save();assertTrue(A.id>0);assertTrue(A.task_progress<100);assertTrue(A.task_status!=Status.SUCCESS);D=TaskDispatcher(Webscrape);D.dispatch(A.task_name,A);sleep(30);assertTrue(A.task_progress>0);assertTrue(A.task_progress<100);assertTrue(A.task_status!=Status.QUEUED);assertTrue(A.task_status!=Status.SUCCESS)