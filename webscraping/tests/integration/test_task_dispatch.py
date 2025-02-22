from django.test import SimpleTestCase, TestCase, TransactionTestCase
from django.db.utils import OperationalError

from webscraping.modules.threader.classes.TaskDispatcher import TaskDispatcher
from webscraping.modules.threader.classes.TaskProgress import Status
from webscraping.models import Webscrape

import re, datetime, time
from typing import Union


class ProcessObject:
    """
        processObj = {
            "title": "A process object with: task_run_id, task_progress, task_outputs",
            "task_run_id": None,
            "task_progress": None,
            "task_outputs": None,
        }
    """
    task_run_id: Union[ str, None ] = None
    task_progress: Union[ int, None ] = None
    task_status: Union[ str, None ] = None
    task_outputs: Union[ list, None] = None
    description: str = "A process object with: task_run_id, task_progress, task_outputs"


class TasksDispatchTestCases(TransactionTestCase):


    @staticmethod
    def _print(key, value):
        print( f'webscraping.tests.integration.test_long_running_task - { key } :: { value }' )


    def test_queue_task(self):
        data = {
            "website_url": "localhost",
            "country": "US",
            "task_name": "localhost-test.sequences/localhost-test.sequence.json",
        }

        webscrape = Webscrape(**data)

        # Get task variables from model fields
        # ------------------------------------
        webscrape.task_variables = model_to_dict(self.webscrape)
        webscrape.save()


        # -------------------
        # Base assertions
        # -------------------
        assertTrue(webscrape.id > 0)
        assertTrue(webscrape.task_progress < 100)
        assertTrue(webscrape.task_status != Status.SUCCESS)

        
        # -------------------
        # Queue task
        # -------------------
        taskDispatcher = TaskDispatcher(Webscrape)
        taskDispatcher.dispatch(
                webscrape.task_name, webscrape)
        sleep(30)


        # -------------------
        # End assertions
        # -------------------
        assertTrue(webscrape.task_progress >= 100)
        assertTrue(webscrape.task_status == Status.SUCCESS)



    def test_queue_task_force_run(self):
        data = {
            "website_url": "localhost",
            "country": "US",
            "task_name": "localhost-test.sequences/localhost-test.sequence.json",
        }

        webscrape = Webscrape(**data)

        # Get task variables from model fields
        # ------------------------------------
        webscrape.task_variables = model_to_dict(self.webscrape)
        webscrape.save()


        # -------------------
        # Base assertions
        # -------------------
        assertTrue(webscrape.id > 0)
        assertTrue(webscrape.task_progress < 100)
        assertTrue(webscrape.task_status != Status.SUCCESS)

        
        # -------------------
        # Queue task
        # -------------------
        taskDispatcher = TaskDispatcher(Webscrape)
        taskDispatcher.dispatch(
                webscrape.task_name, webscrape, force_run=True)
        sleep(30)


        # -------------------
        # End assertions
        # -------------------
        assertTrue(webscrape.task_progress >= 100)
        assertTrue(webscrape.task_status == Status.SUCCESS)





    def test_faling_task(self):
        data = {
            "website_url": "localhost",
            "country": "US",
            "task_name": "localhost-test.sequences/localhost-test-fail.sequence.json",
        }

        webscrape = Webscrape(**data)

        # Get task variables from model fields
        # ------------------------------------
        webscrape.task_variables = model_to_dict(self.webscrape)
        webscrape.save()


        # -------------------
        # Base assertions
        # -------------------
        assertTrue(webscrape.id > 0)
        assertTrue(webscrape.task_progress < 100)
        assertTrue(webscrape.task_status != Status.SUCCESS)

        
        # -------------------
        # Queue task
        # -------------------
        taskDispatcher = TaskDispatcher(Webscrape)
        taskDispatcher.dispatch(
                webscrape.task_name, webscrape)
        sleep(30)


        # -------------------
        # End assertions
        # -------------------
        assertTrue(webscrape.task_progress > 0 100)
        assertTrue(webscrape.task_progress < 100)
        assertTrue(webscrape.task_status != Status.QUEUED)
        assertTrue(webscrape.task_status != Status.SUCCESS)

