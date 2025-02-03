from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils.text import slugify

from django.core.cache import cache
from django.conf import settings

import threading
from time import sleep
from typing import Union

import uuid
from uuid import uuid1

from enum import Enum


class Countries(models.TextChoices):
    """
        Description
            Usage
                view:
                    ```python
                        self.countries = list(zip(Countries.values, Countries.names))
                    ```
                template:
                    ```html
                        <select id="country">
                            <option>Select a country...</option>
                            {% for country in countries %}
                                <option value="{{ country.0 }}">{{ country.1 }}</option>
                            {% endfor %}
                        </select>
                    ```
    """
    CAMEROUN = 'CM', _('Cameroon')
    CANADA = 'CA', _('Canada')
    FRANCE = 'FR', _('France')
    NIGERIA = 'NG', _('Nigeria')
    USA = 'US', _('USA')
    UK = 'UK', _('United Kingdom')


class USStates(models.TextChoices):
    """
        Description
            Usage
                view:
                    ```python
                        self.states = list(zip(USStates.values, USStates.names))
                    ```
                template:
                    ```html
                        <select id="state">
                            <option>Select a state...</option>
                            {% for state in states %}
                                <option value="{{ state.0 }}">{{ state.1 }}</option>
                            {% endfor %}
                        </select>
                    ```
    """
    CALIFORNIA = 'CA', _('California')
    FLORIDA = 'FL', _('Florida')
    NEW_JERSEY = 'NJ', _('New Jersey')
    WASHINGTON = 'WA', _('Washington')
    WINSCONSIN = 'WI', _('Wisconsin')



class WebscrapeTasks(models.TextChoices):
    """
        Description
            Usage
                view:
                    ```python
                        self.webscrape_tasks = list(zip(WebscrapeTasks.values, WebscrapeTasks.names))
                    ```
                template:
                    ```html
                        <select id="task_name" name="task_name">
                            <option>Select a webscrape_task...</option>
                            {% for webscrape_task in webscrape_tasks %}
                                <option value="{{ webscrape_task.0 }}">{{ webscrape_task.1 }}</option>
                            {% endfor %}
                        </select>
                    ```
    """
    TRUTHFINDER_USA_FIND_A_PERSON = 'truthfinder.sequences/find-person-in-usa.sequence.json', \
                                _('TRUTHFINDER - USA: Find a person')
    AFRSCIENCE_AUTEUR_SOUMETTRE_UN_ARTICLE = 'afriscience.sequences/auteur-soumettre-un-article.sequence.json', \
                                _('AFRISCIENCE - AUTEUR: Soumettre un article')



class WebsiteUrls(models.TextChoices):
    """
        Description
            Usage
                view:
                    ```python
                        self.website_urls = list(
                            zip(WebsiteUrls.values, WebsiteUrls.names))
                    ```
                template:
                    ```html
                        <select id="website_url" name="website_url">
                            <option>Select a website...</option>
                            {% for website_url in website_urls %}
                                <option value="{{ website_url.0 }}">{{ website_url.1 }}</option>
                            {% endfor %}
                        </select>
                    ```
    """
    TRUTHFINDER = 'https://www.truthfinder.com', 'truthfinder.com'
    AFRISCIENCE = 'https://app.afriscience.org', 'afriscience.org'



class StatusTextChoices(models.TextChoices):
    STARTED = 'STARTED', _('Started')
    RUNNING = 'RUNNING', _('Running')
    SUCCESS = 'SUCCESS', _('Success')
    FAILED = 'FAILED', _('Failed')


class Webscrape(models.Model):
    # website
    # -------
    # https://www.truthfinder.com/people-search/
    website_url = models.CharField(max_length=200,  choices=WebsiteUrls.choices,
                        default="https://www.truthfinder.com/")
    # metas
    # -----
    title = models.CharField(max_length=200, null=True, blank=True)

    task_name = models.CharField(max_length=200, null=False, blank=False,
                        choices=WebscrapeTasks.choices,
                        default="truthfinder.sequences/find-person-in-usa.sequence.json")
    task_variables = models.JSONField(max_length=200, null=True, blank=True)
    task_id = models.CharField(max_length=50, null=True, blank=True)
    task_progress = models.IntegerField(default=0)
    task_status = models.CharField(max_length=20, null=True, blank=True, choices=StatusTextChoices.choices)
    task_output = models.TextField(null=True, blank=True)

    # identification
    # --------------
    firstName = models.CharField(max_length=200, null=False, blank=False)
    lastName = models.CharField(max_length=200, null=False, blank=False)
    middleName = models.CharField(max_length=200, null=True, blank=True)
    middleInitial = models.CharField(max_length=6, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    # list
    # ----
    by_list = models.TextField(null=True, blank=True)

    # location
    # --------
    city = models.CharField(null=True, blank=True, max_length=200)
    state = models.CharField(null=True, blank=True, max_length=2,  choices=USStates.choices)
    country = models.CharField(null=True, blank=True, max_length=2,  choices=Countries.choices, default="US")

    # parent, foreign
    # ---------------
    parent = models.ForeignKey("Webscrape", null=True, blank=True, 
                            on_delete=models.CASCADE,
                            related_name="webscrape_children", editable=False)

    task_queue = models.ForeignKey("WebscrapeTasksQueue", null=True, blank=True, 
                            on_delete=models.DO_NOTHING,
                            related_name="tasksqueue_webscrapes", editable=False)

    # crud datetimes
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.website_url} - {self.title} - task: {self.task_name} - variables: {self.task_variables}"


    def update_task_status(self):
        """
            Description
            -----------
            If the task is not running anymore and not at 100% with SUCCESS status, marked as failed...
            -    Get webscrape's Taskhandler TaskProgess object
            -    If existing:
                 *    Do nothing, task still running, to be updated
                 *    If not:
                     +    Check if webscrape at 100% with SUCCESS status
                         -    If not:
                             *    Change task_status to FAILED
        """

        taskProgress = TaskHandler.get_taskProgress(self.task_id)
        if not taskProgress and not \
            (self.task_status == Status.SUCCESS.value 
                            and self.task_progress == 100):
            self.task_status = Status.FAILED.value

        name = f"{self.firstName} {self.lastName}"

        token = ""
        if self.task_status == Status.SUCCESS.value:
            token = "✓"
            self.task_queue = None
        else:
            token = "✗"

        if self.by_list and \
                self.task_status in (Status.SUCCESS.value, Status.FAILED.value):
            self.by_list = self.by_list.replace(name, f"{name} {token}")

        self.save()

        if self.parent:
            self.parent.by_list = self.parent.by_list.replace(name, f"{name} {token}")
            self.parent.save()


    def save(self, *args, **kwargs):
        # Custom logic before saving
        # ...

        # Call the "real" save() method
        super().save(*args, **kwargs)


class WebscrapeTasksQueue(models.Model):
    # metas
    # -----
    title = models.CharField(max_length=200, null=True, blank=True, 
                                default="Default task queue")
    description = models.TextField(null=True, blank=True, 
        default="""
            To:
            - Add tasks to queue
            - Check and limit to the number or max concurrent tasks from settings
            The next task in the line is picked up when the previous is completed.
        """
    )

    # crud datetimes
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


    def queue_task(self, webscrape: Webscrape):
        webscrape.task_queue = self
        webscrape.save()


    def pick_next_task(self):
        webscrape.task_queue = self
        webscrape.save()



class StoppableThread(threading.Thread):
    """
        A thread that can be stopped gracefully using a flag.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = threading.Event()  # Flag to signal thread to stop

    def stop(self):
        """
        Signal the thread to stop.
        """
        self._stop_event.set()

    def stopped(self):
        """
        Check if the thread has been signaled to stop.
        """
        return self._stop_event.is_set()

    def run(self):
        """
        Override the run method to periodically check the stop flag.
        """
        while not self.stopped():
            print("Thread is running...")
            sleep(1)  # Simulate work
        print("Thread stopped gracefully.")





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
                    taskProgress.set(
                        Status.STARTED, progress_value,
                        progress_message=f'The webscrape "{webscrape}" has been started'
                    )

                    # Example: Execute web scraping steps
                    for step in webscrape.steps:
                        # Simulate step execution
                        progress_value += 10
                        taskProgress.set(
                            Status.RUNNING, progress_value,
                            progress_message=f'Step {step} has been processed'
                        )

                    # Mark task as completed
                    taskProgress.set(
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

    tasks: dict = {}  # Dictionary to track running tasks: {task_id: thread}
    tasks_queue: list = []  # Queue to hold tasks waiting to be executed


    def __init__(self):
        self.tasks = {}  # Initialize the tasks dictionary


    @staticmethod
    def get_taskProgress( task_id : str ):
        """
            Retrieve the TaskProgress object for a given task_id.

            Args:
                task_id (str): The ID of the task to retrieve.

            Returns:
                TaskProgress: The TaskProgress object associated with the task_id.
        """
        return cache.get( task_id )


    def start_task(self, method, args):
        """
            Start a new background task in a separate thread.

            Args:
                method (callable): The method to execute in the background.
                args (list): Arguments to pass to the method. The first element must be a model
                            with a 'task_id' attribute to track the task.

            Returns:
                str: The task_id of the newly started task.
        """
        taskProgress = TaskProgress(self)
        t = StoppableThread( target=method, args=[ *args, taskProgress ] )
        t.setDaemon(True)
        t.start()

        # Track the task and its thread
        self.tasks[taskProgress.get_task_id()] = t

        return taskProgress.get_task_id()


    def start_next_tasks(self):
        """
            Start the next task in the queue if any tasks are waiting.
        """
        n = settings.WEBSCRAPER_THREADS_MAX

        while len(self.tasks.keys()) <= n:
            if len(self.tasks_queue):
                method, args = self.tasks_queue.pop(0)
                args.task_id = self.start_task(method, args)
                args.save()


    def queue_task(self, method, args):
        """
            Add a task to the queue for later execution.

            Args:
                method (callable): The method to execute in the background.
                args (list): Arguments to pass to the method. The first element must be a model
                            with a 'task_id' attribute to track the task.
        """
        self.tasks_queue.append((method, args))


    def end_task_start_next(self, task_id: str):
        """
            Ends a running task and flush it from memory.
            Starts the next one in queue, if existing...

            Args:
                task_id (str): The ID of the task to terminate.
        """
        if task_id in self.tasks:
            thread = self.tasks[task_id]
            if thread and thread.is_alive():
                # Gracefully terminate the thread using the StoppableThread mechanism
                thread.stop()  # Signal the thread to stop
                thread.join()  # Wait for the thread to finish

                self.start_next_tasks()

            # Remove the task from the tracking dictionary
            del self.tasks[task_id]


class Status(Enum):
    """
        Enum representing the possible statuses of a task.
    """
    STARTED = 'STARTED'
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'


class TaskProgress:
    """
        A class to track the progress of a background task.

        -----------
        Src:
            "A simple approach for background task in Django"
            Handle long running task using Threading and Django Cache
            - https://ivanyu2021.hashnode.dev/a-simple-approach-for-background-task-in-django
    """

    task_id: Union[str, None] = None  # Unique ID for the task
    status: Status = Status.RUNNING  # Current status of the task
    value: Union[int, None] = None  # Progress value (e.g., percentage)
    output: Union[int, None] = None  # Output of the task
    taskHandler: TaskHandler = None  # Reference to the TaskHandler managing this task


    def __init__(self, taskHandler: TaskHandler):
        self.task_id = str( uuid1() )
        cache.set( self.task_id, self, 3600 )
        self.taskHandler = taskHandler


    def set_unset( self,
            status : Status,
            value : int,
            progress_message : Union[ str, None ] = None,
            expires_in : Union[ int, None ] = None
        ) -> object:
        """
        Update the task's status and progress, and manage its cache lifecycle.

        Args:
            status (Status): The new status of the task.
            value (int): The progress value (e.g., percentage).
            progress_message (str, optional): A message describing the progress.
            expires_in (int, optional): The cache expiration time in seconds.

        Returns:
            object: The updated TaskProgress object.
        """

        self.status = status.value
        self.value = value
        self.progress_message = progress_message

        # Flush the task from cache if it is completed
        if status in [Status.SUCCESS, Status.FAILED]:
            cache.delete(self.task_id)  # Remove the task from cache            
            self.taskHandler.end_task_start_next(self.task_id)  # Stop the associated thread, start next task

        elif cache.get( self.task_id):
            if expires_in:
                # Update the task in cache with a new expiration time
                cache.set(self.task_id, self, expires_in)
        else:
            # Set the task in cache with the default or provided expiration time
            cache.set( self.task_id, self, expires_in or settings.WEBSCRAPER_CACHING_DURATION )


    def get_task_id( self ):
        """
        Get the task_id of this task.

        Returns:
            str: The task_id.
        """
        return self.task_id


    def __str__(self):
        return f"{self.task_id} - {self.status} {self.value} {self.outputs}"

