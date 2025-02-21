from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from django.core.cache import cache
from django.conf import settings
from django_app.settings import (
    logger, _print, 
    WEBSCRAPER_TASK_MAX_ATTEMPTS, 
    WEBSCRAPER_THREAD_TIMEOUT
)

from webscraping.models import ThreadTask, Webscrape
from webscraping.modules.threader.classes.TaskProgress import Status
from webscraping.views import webscrape_steps_long_running_method


import threading
from time import sleep
from typing import Union

from datetime import datetime, timedelta
import uuid, copy, json
from uuid import uuid1

from enum import Enum

DEBUG = settings.DEBUG




class TaskDispatcher:
    """
        A class to check and dispatch tasks...

        Example usage:
            ```python

                # Example usage
                task_dispatcher = TaskDispatcher()
                ...
            ```
    """
    taskClass: ThreadTask = None

    def __init__(self, taskClass: ThreadTask):
        self.taskClass = taskClass

    @property
    def taskHandler(self):
        # Task handler from cache
        # ------------------------
        if not _self._taskHandler:
            self._taskHandler = TaskHandler.get_taskHandler(self.taskClass)

        return self._taskHandler



    def check_tasks_to_run(self):
        """
            Querying, then filtering tasks for tasks to run
            Then dispatching them...

            1. Check that status is not QUEUED, RUNNING  or SUCCESS
            2. Check that progress is not 100%
            3. Check that MAX_ATTEMPTS is not reached
            4. 
                if 1, 2, 3: check that task does not have TaskProgress, or that 
                Task thread timeout is reached: 
                  datetime.now – task_thread_started_at >= TASK_TIMEOUT

            Return:
                Dispacthed tasks: Union[List, None]
        """

        # ----------------------------------
        # 1. Check that status is not QUEUED, RUNNING  or SUCCESS
        # 2. Check that progress is not 100%
        # 3. Check that MAX_ATTEMPTS is not reached
        # ----------------------------------
        task_is_queuable_Q = (
              ~Q(task_status__in=["QUEUED", "RUNNING", "SUCCESS"])
            &  Q(task_progress__lt=100)
            &  Q(task_attempts__lt=settings.WEBSCRAPER_TASK_MAX_ATTEMPTS)
        )
        tasks = Webscrape.objects.filter(task_is_queuable_Q)

        # ----------------------------------
        # 4. 
        # if 1, 2, 3: check that task does not have TaskProgress, or that 
        # Task thread timeout is reached: 
        #   datetime.now – task_thread_started_at >= TASK_TIMEOUT
        # ----------------------------------
        def task_is_queuable_f(task):
            # task does not have TaskProgress
            # -------------------------------
            is_queueable = True if not TaskHandler.get_taskProgress(task.task_run_id) else False

            # ... or that task thread timeout is reached
            # -------------------------------------------
            if not is_queueable:
                is_queueable = TaskHandler.task_is_timedout(task)

            return is_queueable

        tasks = list(filter(lambda x: task_is_queuable_f(task), tasks))


        if len(tasks):
            for task in tasks:
                # Dispatch the task based on the value of task_todo
                _Status = self.dispatch(task.task_todo, task)

                # Clear the task_todo field after dispatching
                task.task_status = _Status.value
                task.save()

            msg = self.style.SUCCESS(
                f"\n\n\t\t--------------------------------------------------------"
                f"\n\t\tTask checking and dispatching completed: {len(tasks)} tasks done."
                f"\n\t\t--------------------------------------------------------\n\n"
            )
            self.stdout.write(msg), logger.info(msg)

        return tasks



    def check_tasks_to_end(self, 
            webscrapes: Union[ list[Webscrape], None ] = None,
            status: Union[ Status, None ] = None ):
        """
            For each task with status=(arg:None)
            + for each task in running queue:
            ________________________________


            1. Check if task is completed, or if task has reached timeout:
               - if completed: set task status SUCCESS
               - if timed out: set task status FAILED
               - call `taskHandler.end_task_start_nexts`

            2. if not completed and not timed out:
               - Do nothin, pass
        """

        Queries = {
            # ----------------------------------
            # 1. Check tasks that do not have the status SUCCESS
            #    that are completed, or that have reached timeout:
            #    - if completed: set task status SUCCESS
            # ----------------------------------
            "task_is_completed_Q": ((
                  ~Q(task_status="SUCCESS")
                &  Q(task_progress__gte=100)
            ), Status.SUCCESS.value),

            # ----------------------------------
            # ...
            #   - if timed out: set task status FAILED
            # ----------------------------------
            "task_is_timedout_Q": ((
                  ~Q(task_status="SUCCESS")
                &  Q(task_thread_started_at__lte=(datetime.now() - timedelta(minutes=10)))
            ), Status.FAILED.value)
        }

        tasks = []
        for key in Queries:
            _tuple =Queries[key]
            query = _tuple[0]
            status = _tuple[1]

            _tasks = Webscrape.objects.filter(query)
            for task in _tasks:
                # ----------------------------------
                # ...
                #   - call `taskHandler.end_task`
                # ----------------------------------
                task = self.taskHandler.end_task(
                                    task.task_run_id, taskObject=task)

                # ----------------------------------
                # ...
                #   - save, to finish. Task status must be updated
                #     *after* task is stopped.
                # ----------------------------------
                task.task_status = status
                task.save()
                tasks.append(task)

        if len(tasks):

            msg = self.style.SUCCESS(
                f"\n\n\t\t--------------------------------------------------------"
                f"\n\t\tTask checking completed: {len(tasks)} tasks ended."
                f"\n\t\t--------------------------------------------------------\n\n"
            )
            self.stdout.write(msg), logger.info(msg)

        return tasks


    def dispatch(self, task_name: str, webscrape: Webscrape):
        """
        Dispatches tasks based on the task_name.

        Args:
            task_name (str): The name of the task to execute.
            webscrape (Webscrape): The Webscrape instance associated with the task.
        """
        method = {
            "webscrape_steps_long_running_method": webscrape_steps_long_running_method
        }.get(task_name, ValueError(f"Unknown task: {task_name}"))


        # Queue task with Task handler
        # -----------------------------
        _Status = self.taskHandler.queue_task( method, [ webscrape ] )

        return _Status


