from django.utils.translation import gettext_lazy as _

from django.core.cache import cache
from django.conf import settings
from django_app.settings import (
    logger, _print,
    WEBSCRAPER_THREADS_MAX,
    WEBSCRAPER_TASK_MAX_ATTEMPTS, 
    WEBSCRAPER_THREAD_TIMEOUT
)

from webscraping.modules.threader.classes.StoppableThread import StoppableThread
from webscraping.modules.threader.classes.TaskProgress import TaskProgress, Status

import threading
from time import sleep
from typing import Union

from datetime import datetime, timedelta
import uuid, copy, json
from uuid import uuid1

from enum import Enum

DEBUG = settings.DEBUG




class TaskHandler:
    """
        A class to handle background tasks using threading and Django cache.
        Tasks are tracked and can be stopped gracefully.

        -----------
        Src:
            "A simple approach for background task in Django"
            Handle long running task using Threading and Django Cache
            - https://ivanyu2021.hashnode.dev/a-simple-approach-for-background-task-in-django

        Update:
            Mon 03 Feb 2025 w @Deepseek:
            - Added thread tracking and graceful stopping mechanism using StoppableThread.


        Example usage:
            ```python

                # Long running method
                def webscrape_steps_long_running_method(webscrape: Webscrape, taskProgress):
                    def _print(key, value):
                        print(f'-------| webscrape_steps_long_running_method > {key}', value)

                    progress_value = 0
                    taskProgress.set_unset(
                        Status.STARTED, progress_value,
                        progress_message=f'The webscrape "{webscrape}" has been started'
                    )

                    # Example: Execute web scraping steps
                    for step in webscrape.steps:
                        # Simulate step execution
                        progress_value += 10
                        taskProgress.set_unset(
                            Status.RUNNING, progress_value,
                            progress_message=f'Step {step} has been processed'
                        )

                    # Mark task as completed
                    taskProgress.set_unset(
                        Status.SUCCESS, 100,
                        progress_message=f"Webscrape completed successfully"
                    )


                # Example usage
                task_handler = TaskHandler()
                webscrape = Webscrape.objects.get(id=1)  # Replace with your model instance
                task_handler.queue_task(webscrape_steps_long_running_method, [webscrape])
                task_handler.start_next_tasks()
            ```
    """

    tasks_running: dict = {}  # Dictionary to track running tasks: {task_run_id: thread}
    tasks_queue: list = []  # Queue to hold tasks waiting to be executed

    taskClass = None # type : ThreadTask, or subclass of - @ToDo: Implement inheritance... 


    def __init__(self, taskClass): # type : ThreadTask, or subclass of
        self.tasks_running = {}  # Initialize the running tasks dictionary
        self.taskClass = taskClass


    @staticmethod
    def get_self_cache_key():
        """
            Gets the task handers' cache key, used to retrived and use
            the object or set it in cache

            Returns:
                str: the cache key string
        """
        return settings.WEBSCRAPER_TASKHANDLER_CACHE_KEY


    @staticmethod
    def get_taskHandler(taskClass): # type : ThreadTask, or subclass of
        """
            Gets the current task hander from cache, or instantiates
            a new one and set it in cache.

            Returns:
                TaskHandler: the cache key string
        """

        # Task handler from cache
        # ------------------------
        key = TaskHandler.get_self_cache_key()
        taskHandler = cache.get( key )
        if not taskHandler:
            taskHandler = TaskHandler(taskClass)
            cache.set( key, taskHandler )

        return taskHandler


    @staticmethod
    def get_taskProgress( task_run_id : str ):
        """
            Retrieve the TaskProgress object for a given task_run_id.

            Args:
                task_run_id (str): The ID of the task to retrieve.

            Returns:
                TaskProgress: The TaskProgress object associated with the task_run_id.
        """
        return cache.get( task_run_id )


    @staticmethod
    def task_is_timedout(task): # type : ThreadTask, or subclass of
        task_duration = (datetime.now() - \
                            task.task_thread_started_at).seconds // 60
        
        return task_duration > WEBSCRAPER_THREAD_TIMEOUT



    @staticmethod
    def task_is_queueable(task): # type : ThreadTask, or subclass of

        # 1. Check that status is not QUEUED, RUNNING  or SUCCESS
        # -------------------------------------------------------
        is_queueable = task.task_status not in (Status.QUEUED.value, 
                        Status.RUNNING.value, Status.SUCCESS.value)

        # 2. Check that progress is less than 100%
        # ----------------------------------
        if is_queueable:
            is_queueable = task.task_progress < 100

        # 3. Check that MAX_ATTEMPTS is not reached
        # -------------------------------------------------------
        if is_queueable:
            is_queueable = task.task_attempts < WEBSCRAPER_TASK_MAX_ATTEMPTS


        # 4. if 1, 2, 3: check that task does not have TaskProgress
        # -------------------------------------------------------
        if is_queueable:
            is_queueable = True if not TaskHandler.get_taskProgress(task.task_run_id) else False

            # ... or that task thread timeout is reached
            # -------------------------------------------
            if not is_queueable:
                is_queueable = TaskHandler.task_is_timedout(task)


        # msg = '-------------------------| QUEUABLE TASK ? >> ' \
        #       f'task.task_is_queueable :: {is_queueable}  ///  ' \
        #       'task_status, task_attempts - WEBSCRAPER_TASK_MAX_ATTEMPTS, task_run_id :: ' \
        #       f'{task.task_status}, {task.task_attempts} - ' \
        #       f'{WEBSCRAPER_TASK_MAX_ATTEMPTS}, ' \
        #       f'{task.task_run_id} '

        # _print(msg, VERBOSITY=3), logger.info(msg)

        
        return is_queueable


    def queue_task(self, method, args, force_run = False) -> Status:
        """
            Add a task to the queue for later execution.

            Args:
                method (callable): The method to execute in the background.
                args (list): Arguments to pass to the method. The first element must be a model
                            with a 'task_run_id' attribute to track the task.

            
        """
        task_previously_queued = False
        for _method, _args in self.tasks_queue:
            if _method == method and _args[0].id == args[0].id:
                task_previously_queued = True
                break

        if not task_previously_queued:
            self.tasks_queue.append((method, args))

        if not force_run:

            self.start_next_tasks()

            _message = f"Taskhandler.queue_task - QUEUED :: previously? {task_previously_queued}" \
                       f" /// {method} - {args}"
            _print(_message, VERBOSITY=0)
            logger.debug(_message)

            return Status.QUEUED

        if force_run:

            self.start_task(method, args)

            _message = f"Taskhandler.queue_task - RUNNING :: " \
                       f" /// {method} - {args}"
            _print(_message, VERBOSITY=0)
            logger.debug(_message)

            return Status.RUNNING


    def start_task(self, method, args, taskObject = None): # type : ThreadTask, or subclass of
        """
            Start a new background task in a separate thread.

            Args:
                method (callable): The method to execute in the background.
                args (list): Arguments to pass to the method. The first element must be a model
                            with a 'task_run_id' attribute to track the task.
                taskObject (ThreadTask) (optional):
                            The ThreadClass model or subclass of, instance to for which to start a thread

            Returns:
                str: The task_run_id of the newly started task.
        """
        taskProgress = TaskProgress(self)
        task_run_id = taskProgress.get_task_run_id()

        t = StoppableThread( target=method, args=[ *args, taskProgress ] )

        t.setDaemon(True)
        t.start()

        # Track the task and its thread
        self.tasks_running[task_run_id] = t

        try:
            if not taskObject:
                taskObject = self.taskClass.objects.get(task_run_id=task_run_id)

            if not taskObject.task_attempts:
                taskObject.task_attempts = 0
            taskObject.task_attempts = taskObject.task_attempts + 1

            taskObject.task_status = Status.RUNNING.value
            taskObject.task_thread_started_at = datetime.now()
            taskObject.save()

        except Exception as err:
            logger.error(f"{datetime.now()} - Taskhandler.start_task - taskObject.save() ERROR : {err}")


        logger.debug("Taskhandler.start_task - RUNNING > len(self.tasks_running.keys()) > : %i" % len(self.tasks_running.keys()))

        return task_run_id


    def start_next_tasks(self, forceStartTaskObjects = []):
        """
            Start the next task in the queue if any tasks are waiting.

            Return
                (int, int): number of tasks started, number of tasks runnning
        """        
        msgs = [f"Taskhandler.start_next_tasks - WEBSCRAPER_THREADS_MAX :: {WEBSCRAPER_THREADS_MAX}"]
        msgs.append(f"Taskhandler.start_next_tasks - QUEUED TASKS :: {len(self.tasks_queue)}")
        msgs.append(f"Taskhandler.start_next_tasks - RUNNING TASKS :: {len(self.tasks_running.keys())}")
        for msg in msgs: logger.debug(msg), print(msg)

        i = 0
        while len(self.tasks_running.keys()) <= WEBSCRAPER_THREADS_MAX:
            if len(self.tasks_queue):
                method, args = self.tasks_queue.pop(0)
                obj = args[0]

                if obj.task_attempts < WEBSCRAPER_TASK_MAX_ATTEMPTS:
                    self.start_task(method, args, taskObject=obj)

                    logger.debug("Taskhandler.start_next_tasks - obj SAVED > : %s - %s" % (str(method), str(args)))
                    i += 1 


        return i, len(self.tasks_running.keys())


    def end_task(self, 
                 task_run_id: str, 
                 taskObject = None, # type : ThreadTask, or subclass of
                 do_save: bool = False):
        """
            Ends a running task and flush it from memory.

            Args:
                task_run_id (str): The ID of the task to terminate.
                taskObject (ThreadTask) (optional):
                            The ThreadClass model or subclass of, instance to for which to start a thread
                do_save (book) (optional):
                            if database save should be done here, or not
        """

        # ---------------------------------
        # First start next tasks, so that next thread can run:
        # With this, only individual threads may hang/freeze, not the whole process 
        # ---------------------------------
        self.start_next_tasks()


        try:
            if not taskObject:
                taskObject = self.taskClass.objects.get(task_run_id=task_run_id)
        except Exception as err:
            msg = "Taskhandler.end_task - Exception : %s " % str(err)                    
            _print(msg, VERBOSITY=0), logger.debug(msg)

        if task_run_id in self.tasks_running:
            thread = self.tasks_running[task_run_id]
            if DEBUG:
                logger.debug("Taskhandler.start_next_tasks - thread IS_ALIVE > %s " \
                                                            % (str(thread.is_alive())))
            if thread and thread.is_alive():
                try:

                    # Gracefully terminate the thread using the StoppableThread mechanism
                    # -------------------------------------------------------------------
                    thread.stop()  # Signal the thread to stop

                    # Check if the current thread is not the same as the thread being joined
                    if thread != threading.current_thread():
                        thread.join()  # Wait for the thread to finish
                    else:
                        logger.debug("Cannot join current thread, skipping join")

                except RuntimeError as err:
                    # RuntimeError: cannot join current thread
                    # ----------------------------------------
                    msg = "Taskhandler.end_task - RuntimeError : %s " % str(err)                    
                    _print(msg, VERBOSITY=0), logger.debug(msg)


            # Nullify the thread, and remove the task from the tracking dictionary
            self.tasks_running[task_run_id] = None
            del self.tasks_running[task_run_id]

            if taskObject:
                taskObject.task_thread_stopped_at = datetime.now()
                if do_save:
                    taskObject.save()

            return taskObject


    def end_task_start_next(
                self, 
                task_run_id: str, 
                taskObject = None, # type : ThreadTask, or subclass of
                do_save: bool = False):
        """
            Calls end_task to ends a running task and flush it from memory.
            Starts the next one in queue, if existing...

            Args:
                task_run_id (str): The ID of the task to terminate.
                taskObject (ThreadTask) (optional):
                            The ThreadClass model or subclass of, instance to for which to start a thread
                do_save (book) (optional):
                            if database save should be done here, or not

            Return
                (ThreadTask,    ThreadTask model instance or subclass of
                                for which the thread has been started
                    int, int):  number of tasks started, number of tasks runnning
        """
        taskObject = self.end_task(task_run_id, taskObject=taskObject, do_save=do_save)
        i, n = self.start_next_tasks()
        
        return taskObject, i, n
