from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django_app.settings import (
    logger, WEBSCRAPER_THREAD_TIMEOUT
)
import threading
from time import sleep
from typing import Union

from datetime import datetime, timedelta

DEBUG = settings.DEBUG


class StoppableThread(threading.Thread):
    """
        A thread that can be stopped gracefully using a flag.
    """

    task_run_id: Union[str, None] = None  # Unique ID for the task

    def __init__(
            self, 
            timeout: timedelta = settings.WEBSCRAPER_THREAD_TIMEOUT,
            *args, **kwargs
        ):

        if "args" in kwargs and len(kwargs["args"]) > 1:
            taskProgress = kwargs["args"][1]
            self.task_run_id = taskProgress.get_task_run_id()
        else:
            raise ValueError("Missing or invalid 'args' in kwargs")

        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()  # Flag to signal thread to stop

        self.timeout = timeout  # Timeout duration
        self.start_time = None  # Track when the thread starts


    def stop(self):
        """
        Signal the thread to stop.
        """
        print("Thread with task_run_id '%s': STOP..." % self.task_run_id)
        self._stop_event.set()

    def stopped(self):
        """
        Check if the thread has been signaled to stop.
        """
        b = self._stop_event.is_set()
        if b:
            print("Thread with task_run_id '%s' is STOPPING..." % self.task_run_id)
        return self._stop_event.is_set()

    def run(self):
        """
        Override the run method to periodically check the stop flag.
        """
        try:
            super().run()

            if self.start_time is None:
                self.start_time = datetime.now()  # Record the start time

            while not self.stopped():
                # Check if the timeout has been reached
                _now = datetime.now()
                logger.debug("StoppableThread.run with task_run_id '%s' - "
                             "NOW / START_TIME : %s / %s" \
                             % (self.task_run_id, _now, self.start_time))

                if _now - self.start_time > self.timeout:

                    logger.debug("Thread with task_run_id '%s' stopping due to timeout..." % (self.task_run_id))
                    print(f"Thread w task_run_id '{self.task_run_id}' stopping due to timeout...")

                    self.stop()  # Signal the thread to stop
                    break
                else:
                    # Simulate work
                    print("Thread with task_run_id '%s' is RUNNING..." % self.task_run_id)
                    sleep(5)  # Sleep between checks...

            print("Thread stopped gracefully.")

        except Exception as e:
            msg = f"Error in thread {self.task_run_id}: {e}"
            logger.debug(msg)
            logger.error(msg)

            self.stop()

            print("Thread stopped gracefully due to an error.")

