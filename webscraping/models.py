from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils.text import slugify

from django.core.cache import cache
from django.conf import settings


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
    RUNNING = 'RUNNING', _('Running')
    SUCCESS = 'SUCCESS', _('Success')
    FAILED = 'FAILED', _('Failed')
    QUEUED = 'QUEUED', _('Queued')
    STARTED = 'STARTED', _('Started')


class WebscrapeTaskNameChoices(models.TextChoices):
    WEBSCRAPE_STEPS = 'webscrape_steps_long_running_method', \
                      'Webscrape detailed process steps long running method...'



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



class ThreadTask(models.Model):

    # optional
    task_title = models.CharField(max_length=200, null=True, blank=True)

    # core
    task_run_id = models.CharField(max_length=50, null=True, blank=True)
    task_progress = models.IntegerField(default=0)
    task_status = models.CharField(max_length=20, null=True, blank=True, choices=StatusTextChoices.choices)
    task_output = models.TextField(null=True, blank=True)
    task_thread_started_at = models.DateTimeField(null=True, blank=True) 
    task_thread_stopped_at = models.DateTimeField(null=True, blank=True) 
    task_attempts = models.IntegerField(default=0)

    # crud datetimes
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"title: {self.task_title} - run_id: {self.task_run_id} " \
               f"- progress: {self.task_progress} - attempts: {self.task_attempts}"


    def save(self, *args, **kwargs):
        # Custom logic before saving
        # ...

        # Call the "real" save() method
        super().save(*args, **kwargs)


    def update_ended_task_status(self):
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

            ----------------------------
            **The Task Lifecycle**

            1.  Task is requested from ui frontend, either as individual, or in batch
            2.  Task is sent to be queued in corresponding uip backend (manage_*.py)
            3.  Task is mark as queued in uip backend webscrape.py
            3.  Task is dequeued by Taskhandler when its time comes
            4.  Task runs, and:
                - is marked as succesfull in long running view function when succeeds
                - is marked as failed in long running view function if fails

            5.  Task is picked and queued in uip backend (table.py) if:
                - not succesful
                - not queued
                - and nr of max attempts not reached...
            6.  Task if checked for timeout, hanging... in model. If:
                - Task has no taskProgress 
                - Task is not marked as successful or task_progress not = 100 
                Task is marked as failed
        """

        taskProgress = TaskHandler.get_taskProgress(self.task_run_id)
        if not taskProgress:
            # Task not running anymore = Task is ended
            # ----------------------------------------

            if self.task_progress >= 100 \
                and self.task_status != StatusTextChoices.SUCCESS.value:
                # Task has succeeded, but status is not updated
                # ----------------------------------------
                self.task_status = StatusTextChoices.SUCCESS.value
                self.save()

            if self.task_progress <= 100 \
                and self.task_status != StatusTextChoices.FAILED.value:
                # Task has failed, but status is not updated
                # ----------------------------------------
                self.task_status = StatusTextChoices.FAILED.value
                self.save()



class Webscrape(ThreadTask):
    # website
    # -------
    # https://www.truthfinder.com/people-search/
    website_url = models.CharField(max_length=200,  choices=WebsiteUrls.choices,
                        default="https://www.truthfinder.com/")
    # metas
    # -----
    task_name = models.CharField(max_length=200, null=False, blank=False,
                        choices=WebscrapeTasks.choices,
                        default="truthfinder.sequences/find-person-in-usa.sequence.json")
    task_variables = models.JSONField(max_length=200, null=True, blank=True)
    task_todo = models.CharField(max_length=100, null=True, blank=True, choices=WebscrapeTaskNameChoices.choices,
                                 help_text="The task to be performed for this web scraping job.")


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


    def __str__(self):
        return f"{self.website_url} - {self.title} - task: {self.task_name} - variables: {self.task_variables}"


    def save(self, *args, **kwargs):
        # Custom logic before saving
        # ...

        # Call the "real" save() method
        super().save(*args, **kwargs)


    def update_ended_task_status(self):
        """
            Description
            -----------
            Update the tasks by_list corresponding [firtName] [lastName] line items:
            -   parent tasks: task has by_list, update items
            -   child task: task has parent, get parent's by_list and update items
            -   save: save only if changed
    
            ----------------------------
            **The Task Lifecycle**

            1.  Task is requested from ui frontend, either as individual, or in batch
            2.  Task is sent to be queued in corresponding uip backend (manage_*.py)
            3.  Task is mark as queued in uip backend webscrape.py
            3.  Task is dequeued by Taskhandler when its time comes
            4.  Task runs, and:
                - is marked as succesfull in long running view function when succeeds
                - is marked as failed in long running view function if fails

            5.  Task is picked and queued in uip backend (table.py) if:
                - not succesful
                - not queued
                - and nr of max attempts not reached...
            6.  Task if checked for timeout, hanging... in model. If:
                - Task has no taskProgress 
                - Task is not marked as successful or task_progress not = 100 
                Task is marked as failed
        """

        # -----------
        # call parent method
        # ------------------
        super.update_ended_task_status()


        # -----------
        # do self method
        # -----------

        def get_line(lines, name):
            line = list(filter(lambda x: x.find(f"{self.firstName} {self.lastName}") >= 0, lines))
            if len(line):
                return line[0]        

        def line_has_token(by_list, name, token):
            lines = by_list.splitlines()
            line = get_line(lines, firstName, lastName)
            return line.find(token) > 0 

        def add_token_and_return(by_list, name, token):
            return by_list.replace(name, f"{name} {token}") 

        name = f"{self.firstName} {self.lastName}"

        token = ""
        if self.task_status == StatusTextChoices.SUCCESS.value:
            token = "✓"
            self.task_queue = None
        else:
            token = "✗"

        if self.by_list and \
                self.task_status in (StatusTextChoices.SUCCESS.value, StatusTextChoices.FAILED.value):
            # Self is parent task, update child's by_list line
            # ------------------------------------------------

            if not line_has_token(self.by_list, name, token) > 0:
                # line does not have token, set and update
                # ----------------------------------------
                self.by_list = add_token_and_return(self.by_list, name, token)
                self.save()

        if self.parent:
            # Self is child task, update parent's by_list self's line
            # ------------------------------------------------------

            if not line_has_token(self.by_list, name, token) > 0:
                # line does not have token, set and update
                # ----------------------------------------
                self.parent.by_list = add_token_and_return(self.parent.by_list, name, token)
                self.save()


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
    def data_for_export_output_to_csv(task_run_id):

        # Step 1: Retrieve the Webscrape object using the provided task_run_id
        # ---------------------------------------------------------
        webscrape = Webscrape.objects.get(task_run_id=task_run_id)

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

