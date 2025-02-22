from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from django.core.cache import cache
from django.conf import settings
from django_app.settings import (
    logger, _print, 
    WEBSCRAPER_TASK_MAX_ATTEMPTS, 
    WEBSCRAPER_THREAD_TIMEOUT,
    WEBSCRAPER_THREAD_TIMEOUT_FROM_CREATION
)

from webscraping.models import ThreadTask, Webscrape
from webscraping.modules.threader.classes.TaskHandler import TaskHandler
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

    _taskHandler = None
    @property
    def taskHandler(self):
        # Task handler from cache
        # ------------------------
        if not self._taskHandler:
            self._taskHandler = TaskHandler.get_taskHandler(self.taskClass)

        return self._taskHandler



    def check_tasks_to_queue(self,
            timeout: timedelta = None ):
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
        started_at_to = timeout or WEBSCRAPER_THREAD_TIMEOUT
        created_on_to = timeout or WEBSCRAPER_THREAD_TIMEOUT_FROM_CREATION

        # ----------------------------------
        # I. ALL TASKS THAT ARE NOT QUEUED, NOT RUNNING, AND NOT SUCCESSFUL
        #
        # 1. Check that status is not QUEUED, RUNNING  or SUCCESS
        # 2. Check that progress is not 100%
        # 3. Check that MAX_ATTEMPTS is not reached
        # ----------------------------------
        task_is_queuable_Q1 = (
              ~Q(task_status__in=["QUEUED", "RUNNING", "SUCCESS"])
            &  Q(task_progress__lt=100)
            &  Q(task_attempts__lt=settings.WEBSCRAPER_TASK_MAX_ATTEMPTS)
        )

        # ----------------------------------
        # II. ALL TASKS THAT HAVE TIMED OUT, AND ARE NOT QUEUED, AND NOT SUCCESSFUL
        #
        # 1. Check that status is not QUEUED, or SUCCESS
        # 2. Check that progress is not 100%
        # 3. Check that MAX_ATTEMPTS is not reached
        # ----------------------------------
        task_is_queuable_Q2 = (
              ~Q(task_status__in=["QUEUED", "SUCCESS"])
            &  Q(task_progress__lt=100)
            &  Q(task_attempts__lt=settings.WEBSCRAPER_TASK_MAX_ATTEMPTS)
            &  (
                Q(task_thread_started_at__lt=(datetime.now() - started_at_to))
                | Q(created_on__lt=(datetime.now() - created_on_to))
            )
        )


        tasks = self.taskClass.objects.filter((task_is_queuable_Q1 | task_is_queuable_Q2))


        if len(tasks):
            for task in tasks:
                # Dispatch the task based on the value of task_todo
                _Status = self.dispatch(task.task_todo, task)

                # Clear the task_todo field after dispatching
                task.task_status = _Status.value
                task.save()

        msg =  \
            f"\n\n\t\t--------------------------------------------------------" \
            f"\n\t\tTASKS TO QUEUE: checking and dispatching completed: {len(tasks)} tasks done." \
            f"\n\t\t--------------------------------------------------------\n\n" \

        print(msg), logger.info(msg)

        return tasks




    def dequeue_and_run(self):
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
        # ALL TASKS THAT ARE QUEUED AND NOT SUCCESSFUL
        #
        # 1. Check that status is QUEUED
        # 2. Check that progress is not 100%
        # 3. Check that MAX_ATTEMPTS is not reached
        # ----------------------------------
        task_is_queuable_Q = (
               Q(task_status__in=["QUEUED"])
            &  Q(task_progress__lt=100)
            &  Q(task_attempts__lt=settings.WEBSCRAPER_TASK_MAX_ATTEMPTS)
        )
        tasks = self.taskClass.objects.filter((task_is_queuable_Q))

        if len(tasks):
            for task in tasks:
                # Dispatch the task based on the value of task_todo
                _Status = self.dispatch(task.task_todo, task)

                # Clear the task_todo field after dispatching
                task.task_status = _Status.value
                task.save()

        msg =  \
            f"\n\n\t\t--------------------------------------------------------" \
            f"\n\t\tTASKS TO DEQUEUE AND RUN: checking and dispatching completed: {len(tasks)} tasks done." \
            f"\n\t\t--------------------------------------------------------\n\n" \

        print(msg), logger.info(msg)

        return tasks



    def check_tasks_to_end(self, 
            _which: str,        # "update" | "end"
            webscrapes: Union[ list[Webscrape], None ] = None,
            status: Union[ Status, None ] = None,
            timeout: timedelta = None ):
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

        started_at_to = timeout or WEBSCRAPER_THREAD_TIMEOUT
        created_on_to = timeout or WEBSCRAPER_THREAD_TIMEOUT_FROM_CREATION

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
                &  (
                    Q(task_thread_started_at__lt=(datetime.now() - started_at_to))
                    | Q(created_on__lt=(datetime.now() - created_on_to))
                )
            ), Status.FAILED.value)
        }

        tasks = []
        nc = 0           # n completed
        nto = 0          # n timedout
        i, n = 0, 0      # i started, n running
        for key in Queries:            
            _tuple =Queries[key]
            query = _tuple[0]
            status = _tuple[1]

            _tasks = self.taskClass.objects.filter(query)
            for task in _tasks:

                if _which == "update":
                    # ----------------------------------
                    # ...
                    #   - save, to finish. Task status must be updated
                    #     *before* calling for thread stop (to avoid delayed 
                    #      update because of a hanging thread).
                    # ----------------------------------
                    task.task_status = status
                    task.save()

                elif _which == "end":
                    # ----------------------------------
                    # ...
                    #   - call `taskHandler.end_task_start_next`
                    # ----------------------------------
                    task, i1, n1 = self.taskHandler.end_task_start_next(
                                        task.task_run_id, taskObject=task)
                    i += i1
                    n += n1

                if key == "task_is_completed_Q":
                    nc += 1
                elif key == "task_is_timedout_Q":
                    nto += 1

                tasks.append(task)


        msg = \
            f"\n\n\t\t--------------------------------------------------------" \
            f"\n\t\tTASKS TO {_which.upper()}: checking completed::" \
            f"\n\t\t- {nc} tasks completed" \
            f"\n\t\t- {nto} tasks timed out" \
            f"\n\t\t- {len(tasks)} tasks ended, {i} started, {n} running..." \
            f"\n\t\t--------------------------------------------------------\n\n"

        print(msg), logger.info(msg)

        return tasks


    def dispatch(self, task_name: str, webscrape: Webscrape, force_run = False):
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
        _Status = self.taskHandler.queue_task( 
            method, [ webscrape ],
            force_run = force_run
        )

        return _Status


