from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils.text import slugify

from django.core.cache import cache
from django.conf import settings
from django_app.settings import logger, _print

import threading
from time import sleep
from typing import Union

from datetime import datetime, timedelta
import uuid, copy, json
from uuid import uuid1

from enum import Enum

DEBUG = settings.DEBUG


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
    TRUTHFINDER =  'truthfinder.com', 'https://www.truthfinder.com'
    AFRISCIENCE = 'afriscience.org', 'https://app.afriscience.org'
    LOCALHOST = 'localhost', 'http://localhost:8001'



class StatusTextChoices(models.TextChoices):
    STARTED = 'STARTED', _('Started')
    RUNNING = 'RUNNING', _('Running')
    SUCCESS = 'SUCCESS', _('Success')
    FAILED = 'FAILED', _('Failed')


class WebscrapeTaskNameChoices(models.TextChoices):
    WEBSCRAPE_STEPS = 'webscrape_steps_long_running_method', \
                      'Webscrape detailed process steps long running method...'


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
    task_todo = models.CharField(max_length=100, null=True, blank=True, choices=WebscrapeTaskNameChoices.choices,
                                 help_text="The task to be performed for this web scraping job.")
    task_attempts = models.IntegerField(default=0)


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


    def save(self, *args, **kwargs):
        # Custom logic before saving
        # ...

        # Call the "real" save() method
        super().save(*args, **kwargs)


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


    @staticmethod
    def parse_output_text(
            text: str = '',
            file_path: str = '',
            start_line: int = 8) -> list:
        """
            Parses the output text or file content into a list of dictionaries.

            Args:
                text (str, optional): The text to parse. Defaults to ''.
                file_path (str, optional): The path to the file containing the text to parse. Defaults to ''.
                start_line (int, optional): The line number from which to start parsing. Defaults to 8.

            Returns:
                list: A list of dictionaries, where each dictionary represents a parsed record.

            Raises:
                ValueError: If neither `text` nor `file_path` is provided.

            Steps:
                1. Define a template for the result dictionary.
                2. Read lines from the provided text or file.
                3. Clean and filter the lines to remove unwanted content.
                4. Parse the cleaned lines into dictionaries using the result template.
                5. Return the list of parsed dictionaries.

            Example Usage:
                ```python
                text = "Name: John Doe\nAge: 30\nLocation: New York"
                parsed_data = Webscrape.parse_output_text(text=text)
                print(parsed_data)
                ```

            With:
                Deepseek AI - "Django/Python" conversation → Mon 10 Feb 2025        
        """

        # Step 1: Define a template for the result dictionary
        # ---------------------------------------------------
        result_template = {
            "NAME": None,
            "AGE": None,
            "LOCATION": None,
            "POSSIBLE_RELATIVES": None,
            "VERIFIED": None,
            "CRIMINAL_RECORDS": None,
        }


        # Step 2: Read lines from the provided text or file
        # ---------------------------------------------------
        def read_filelines(file):
            """Reads lines from a file."""
            with open(file) as f:
                return f.readlines()

        lines = []
        if not text and not file_path:
            raise ValueError(
                "webscraping.Webscrape.parse_output_text :: "
                "One of <text> or <file_path> must be provided..."
            )
        elif text:
            lines = text.splitlines()  # Split text into lines
        else:
            lines = read_filelines(file_path)  # Read lines from file


        # Step 3: Clean and filter the lines to remove unwanted content
        # ---------------------------------------------------
        lines = list(map(lambda x: x.replace('\n', '').replace('\t', ''), lines))  # Remove newlines and tabs
        lines = list(filter(lambda x: x.find('We could uncover') < 0, lines))  # Filter out unwanted lines
        lines = list(filter(lambda x: x.find('OPEN REPORT') < 0, lines))  # Filter out unwanted lines
        lines = list(filter(lambda x: x.find('ⓘ') < 0, lines))  # Filter out unwanted lines
        lines = lines[start_line:]  # Skip the first `start_line` lines


        # Step 4: Parse the cleaned lines into dictionaries using the result template
        # ---------------------------------------------------
        results = []
        line_dict = copy.copy(result_template)  # Create a copy of the template for each record
        for line in lines:
            if len(line) >= 2:
                if line.find("Based on your input") >= 0:
                    # Save the current dictionary and start a new one
                    results.append(line_dict)
                    line_dict = copy.copy(result_template)
                elif line.find("Possible Criminal or Traffic") >= 0:
                    line_dict["CRIMINAL_RECORDS"] = True
                elif line.lower().find("verified") >= 0:
                    line_dict["VERIFIED"] = True
                elif line.lower().find(",") >= 0:
                    if not line_dict["LOCATION"]:
                        line_dict["LOCATION"] = []
                    line_dict["LOCATION"].append(line)
                elif len(line) == 2:
                    line_dict["AGE"] = line
                else:
                    if not line_dict["NAME"]:
                        line_dict["NAME"] = line
                    else:
                        if not line_dict["POSSIBLE_RELATIVES"]:
                            line_dict["POSSIBLE_RELATIVES"] = []
                        line_dict["POSSIBLE_RELATIVES"].append(line)


        # Step 5: Return the list of parsed dictionaries
        # ---------------------------------------------------
        return results


    @staticmethod
    def data_for_export_output_to_csv(task_id):

        # Step 1: Retrieve the Webscrape object using the provided task_id
        # ---------------------------------------------------------
        webscrape = Webscrape.objects.get(task_id=task_id)

        # Step 2: Parse the task_output field (assumed to be JSON) into a Python object
        # ---------------------------------------------------------
        task_output = webscrape.task_output
        task_output = task_output.replace("'", '"').replace('\\xa0', '')  # Clean the JSON string
        _jsonObj = json.loads(task_output)  # Convert JSON string to Python object
        task_output = _jsonObj[0]['returned']  # Extract the relevant data


        # Step 3: Process the parsed output to extract relevant data
        # ----------------------------------------------------------
        data: list[ dict ] = Webscrape.parse_output_text(task_output, start_line=0)

        # Step 4: Return the result data
        # ------------------------------
        return data


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


class WebscrapeData(models.Model):
    """
        Model to store web scraping data in a flexible JSON format.

        Fields:
            - title: A short title for the web scraping task.
            - description: A detailed description of the task or its purpose.
            - json_data: A JSON field to store flexible web scraping data.
            - created_on: The date and time when the record was created.
            - last_modified: The date and time when the record was last modified.

        Purpose:
            This model is designed to store web scraping results in a flexible JSON format,
            allowing for easy storage and retrieval of structured or unstructured data.
            It can be used to save data such as:
                - Scraped website content
                - Metadata about the scraping process
                - Results of data extraction or transformation

        With:
            Deepseek AI - "Django/Python" conversation → Mon 10 Feb 2025
    """

    # Title and Description
    title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default="Webscraping Task"
    )
    description = models.TextField(
        null=True,
        blank=True,
        default="""
            For scraping data from specified sources and saving the results
            in a structured JSON format. The data may include:
                - Extracted text, images, or links
                - Metadata about the scraping process
                - Results of data transformation or analysis
            The JSON format allows for flexible storage and easy retrieval of the scraped data.
        """
    )

    # JSON Data Field
    json_data = models.JSONField(
        null=True,
        blank=True,
        default=dict,
        help_text="Flexible JSON field to store web scraping results."
    )

    # CRUD Datetimes
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the model instance.
        """
        return f"{self.title} (Created: {self.created_on})"

    def save(self, *args, **kwargs):
        """
        Override the save method to ensure JSON data is properly formatted.
        """
        if isinstance(self.json_data, str):
            try:
                self.json_data = json.loads(self.json_data)  # Convert string to JSON
            except json.JSONDecodeError:
                self.json_data = {}  # Fallback to empty dict if invalid JSON
        super().save(*args, **kwargs)


    @staticmethod
    def periodic_save_aggregated_results(aggregated_results: dict):
        """
            Periodically saves aggregated results to the WebscrapeData model if the last modification
            was more than 1 hour ago.

            Args:
                aggregated_results (dict): The aggregated results to save.

            Steps:
                1. Retrieve the first WebscrapeData instance from the database.
                2. If no instance exists, create a new one.
                3. Calculate the time difference between the current time and the last modification time.
                4. If the time difference is greater than or equal to 1 hour, update the json_data field
                   and save the instance.

            With:
                Deepseek AI - "Django/Python" conversation → Mon 10 Feb 2025        
        """

        # Step 1: Retrieve the first WebscrapeData instance
        # -------------------------------------------------
        webscrapeData = WebscrapeData.objects.first()


        # Step 2: If no instance exists, create a new one
        # -------------------------------------------------
        if not webscrapeData:
            webscrapeData = WebscrapeData(
                title="Aggregated Results",
                description="Automatically saved aggregated results.",
                json_data=aggregated_results
            )
            webscrapeData.save()


        # Step 3: Calculate the time difference
        # -------------------------------------------------
        _now = datetime.now()
        _delta = _now - webscrapeData.last_modified.replace(tzinfo=None)  # Remove timezone info for comparison


        # Step 4: Check if the time difference is greater than or equal to 1 hour
        # -------------------------------------------------
        if _delta.total_seconds() >= 3600:  # 3600 seconds = 1 hour
            # Update the json_data field with the aggregated results
            webscrapeData.json_data = aggregated_results
            webscrapeData.save()


    @staticmethod
    def data_for_export_output_to_csv(data_id):
        # Retrieve the WebscrapeData object using
        # the provided data_id and return it
        # ---------------------------------------------------------
        webscrapeData = WebscrapeData.objects.get(id=data_id)
        print('-------------------------------| webscrapeData.json_data', webscrapeData.json_data)
        return webscrapeData.json_data



class StoppableThread(threading.Thread):
    """
        A thread that can be stopped gracefully using a flag.
    """

    task_id: Union[str, None] = None  # Unique ID for the task

    def __init__(
            self, 
            timeout: timedelta = settings.WEBSCRAPER_THREAD_TIMEOUT,
            *args, **kwargs
        ):

        if "args" in kwargs and len(kwargs["args"]) > 1:
            taskProgress = kwargs["args"][1]
            self.task_id = taskProgress.get_task_id()
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
        print("Thread with task_id '%s': STOP..." % self.task_id)
        self._stop_event.set()

    def stopped(self):
        """
        Check if the thread has been signaled to stop.
        """
        b = self._stop_event.is_set()
        if b:
            print("Thread with task_id '%s' is STOPPING..." % self.task_id)
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
                logger.debug("StoppableThread.run with task_id '%s' - "
                             "NOW / START_TIME : %s / %s" \
                             % (self.task_id, _now, self.start_time))

                if _now - self.start_time > self.timeout:

                    logger.debug("Thread with task_id '%s' stopping due to timeout..." % (self.task_id))
                    print(f"Thread w task_id '{self.task_id}' stopping due to timeout...")

                    self.stop()  # Signal the thread to stop
                    break
                else:
                    # Simulate work
                    print("Thread with task_id '%s' is RUNNING..." % self.task_id)
                    sleep(5)  # Sleep between checks...

            print("Thread stopped gracefully.")

        except Exception as e:
            msg = f"Error in thread {self.task_id}: {e}"
            logger.debug(msg)
            logger.error(msg)

            self.stop()

            print("Thread stopped gracefully due to an error.")




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
        logger.debug("Taskhandler.start_task - TO BE STARTED > len(self.tasks.keys()) > : %i" % len(self.tasks.keys()))

        taskProgress = TaskProgress(self)
        task_id = taskProgress.get_task_id()

        t = StoppableThread( target=method, args=[ *args, taskProgress ] )

        logger.debug("Taskhandler.start_task - STARTING > len(self.tasks.keys()) > : %i" % len(self.tasks.keys()))

        t.setDaemon(True)
        t.start()

        logger.debug("Taskhandler.start_task - STARTED > len(self.tasks.keys()) > : %i" % len(self.tasks.keys()))

        # Track the task and its thread
        self.tasks[task_id] = t

        logger.debug("Taskhandler.start_task - RUNNING > len(self.tasks.keys()) > : %i" % len(self.tasks.keys()))

        return task_id


    def start_next_tasks(self):
        """
            Start the next task in the queue if any tasks are waiting.
        """
        n = settings.WEBSCRAPER_THREADS_MAX
        logger.debug("Taskhandler.start_next_tasks - settings.WEBSCRAPER_THREADS_MAX :: %i" % n)
        logger.debug("Taskhandler.start_next_tasks - len(self.tasks.keys()) :: %i" % len(self.tasks.keys()))

        while len(self.tasks.keys()) <= n:
            if len(self.tasks_queue):
                method, args = self.tasks_queue.pop(0)
                obj = args[0]
                obj.task_id = self.start_task(method, args)
                obj.save()
                logger.debug("Taskhandler.start_next_tasks - obj SAVED > : %s - %s" % (str(method), str(args)))


    def queue_task(self, method, args):
        """
            Add a task to the queue for later execution.

            Args:
                method (callable): The method to execute in the background.
                args (list): Arguments to pass to the method. The first element must be a model
                            with a 'task_id' attribute to track the task.
        """
        _message = "Taskhandler.queue_task - QUEUED > : %s - %s" % (str(method), str(args))
        _print(_message, VERBOSITY=0)
        logger.debug(_message)
        self.tasks_queue.append((method, args))
        self.start_next_tasks()


    def end_task_start_next(self, task_id: str):
        """
            Ends a running task and flush it from memory.
            Starts the next one in queue, if existing...

            Args:
                task_id (str): The ID of the task to terminate.
        """
        if task_id in self.tasks:
            thread = self.tasks[task_id]
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

                    if DEBUG:
                        webscrape = Webscrape.objects.get(task_id=task_id)
                        logger.debug("Taskhandler.start_next_tasks - ENDED > %s ||||||||||||||||| STATUS > %s" \
                                    % (str(webscrape.task_variables), str(webscrape.task_status)))

                except RuntimeError as err:
                    # RuntimeError: cannot join current thread
                    # ----------------------------------------
                    msg = "Taskhandler.start_next_tasks - Err : %s " % str(err)
                    logger.debug(msg)
                    _print(msg, VERBOSITY=0)

                self.start_next_tasks()

            # Nullify the thread, and remove the task from the tracking dictionary
            self.tasks[task_id] = None
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

        self.status = status.value
        self.value = value
        self.progress_message = progress_message

        # Flush the task from cache if it is completed
        if status in [Status.SUCCESS.value, Status.FAILED.value]:
            self.taskHandler.end_task_start_next(self.task_id)  # Stop the associated thread, start next task
            cache.delete(self.task_id)  # Remove the task from cache            

        elif cache.get( self.task_id):
            if expires_in:
                # Update the task in cache with a new expiration time
                cache.set(self.task_id, self, expires_in)
        else:
            # Set the task in cache with the default or provided expiration time
            cache.set( self.task_id, self, expires_in or settings.WEBSCRAPER_CACHING_DURATION )

        if _print_progress:
            _print(self.progress_message)


    def get_task_id( self ):
        """
        Get the task_id of this task.

        Returns:
            str: The task_id.
        """
        return self.task_id


    def __str__(self):
        return f"{self.task_id} - {self.status} {self.value} {self.outputs}"

