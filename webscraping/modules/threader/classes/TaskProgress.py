from django.utils.translation import gettext_lazy as _

from django.core.cache import cache
from django.conf import settings
from django_app.settings import (
    logger, _print, 
    WEBSCRAPER_CACHING_DURATION
)


import threading
from time import sleep
from typing import Union

from datetime import datetime, timedelta
import uuid, copy, json
from uuid import uuid1

from enum import Enum

DEBUG = settings.DEBUG



class Status(Enum):
    """
        Enum representing the possible statuses of a task.
    """
    RUNNING = 'RUNNING'
    QUEUED = 'QUEUED'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    STARTED = 'STARTED'



class TaskProgress:
    """
        A class to track the progress of a background task.

        -----------
        Src:
            "A simple approach for background task in Django"
            Handle long running task using Threading and Django Cache
            - https://ivanyu2021.hashnode.dev/a-simple-approach-for-background-task-in-django
    """

    task_run_id: Union[str, None] = None  # Unique ID for the task
    status: Status = Status.RUNNING  # Current status of the task
    value: Union[int, None] = None  # Progress value (e.g., percentage)
    output: Union[int, None] = None  # Output of the task
    taskHandler = None  # Reference to the TaskHandler instance managing this task


    def __init__(self, taskHandler):
        self.task_run_id = str( uuid1() )
        cache.set( self.task_run_id, self, 3600 )
        self.taskHandler = taskHandler


    def set_unset( self,
            status : Status,
            value : int,
            progress_message : Union[ str, None ] = None,
            expires_in : Union[ int, None ] = None,
            _print_progress: bool = True
        ) -> object:
        """
        Update the task's status and progress, and manage its cache lifecycle.

        Args:
            status (Status): The new status of the task.
            value (int): The progress value (e.g., percentage).
            progress_message (str, optional): A message describing the progress.
            expires_in (int, optional): The cache expiration time in seconds.
            _print (bool, optional): Print progress message.

        Returns:
            object: The updated TaskProgress object.
        """

        self.status = status
        self.value = value
        self.progress_message = progress_message

        # Flush the task from cache if it is completed, or to be retried
        if status.value in [Status.SUCCESS.value, Status.FAILED.value]:
            self.taskHandler.end_task_start_next(self.task_run_id)  # Stop the associated thread, start next task
            cache.delete(self.task_run_id)  # Remove the task from cache            

        elif cache.get( self.task_run_id):
            if expires_in:
                # Update the task in cache with a new expiration time
                cache.set(self.task_run_id, self, expires_in)
        else:
            # Set the task in cache with the default or provided expiration time
            cache.set( self.task_run_id, self, expires_in or settings.WEBSCRAPER_CACHING_DURATION )

        if _print_progress:
            _print(self.progress_message)


    def get_task_run_id( self ):
        """
        Get the task_run_id of this task.

        Returns:
            str: The task_run_id.
        """
        return self.task_run_id


    def __str__(self):
        return f"{self.task_run_id} - {self.status} {self.value} {self.outputs}"

