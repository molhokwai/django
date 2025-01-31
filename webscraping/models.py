from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils.text import slugify

from django.core.cache import cache
from django.conf import settings

import threading
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

    # parent
    # ------
    parent = models.ForeignKey("Webscrape", null=True, blank=True, 
                            on_delete=models.CASCADE,
                            related_name="webscrape_children", editable=False)

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

        line = f"{self.firstName} {self.lastName}"
        token = "✓" if self.task_status == Status.SUCCESS.value else "✗"
        if self.by_list and \
            self.task_status in (Status.SUCCESS.value, Status.FAILED.value):

            self.by_list = self.by_list.replace(line, f"{line} {token}")

        self.save()

        if self.parent:
            self.parent.by_list = self.parent.by_list.replace(line, f"{line} {token}")
            self.parent.save()


class TaskHandler:
    """
        -----------
        Src:
            "A simple approach for background task in Django"
            Handle long running task using Threading and Django Cache
            - https://ivanyu2021.hashnode.dev/a-simple-approach-for-background-task-in-django
    """

    def start_task(self, method, args):

        taskProgress = TaskProgress()
        t = threading.Thread( target=method, args=[ *args, taskProgress ] )
        t.setDaemon(True)
        t.start()

        return taskProgress.get_task_id()

    @staticmethod
    def get_taskProgress( task_id : str ):
        return cache.get( task_id )



class Status(Enum):
    STARTED = 'STARTED'
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'


class TaskProgress:
    """
        -----------
        Src:
            "A simple approach for background task in Django"
            Handle long running task using Threading and Django Cache
            - https://ivanyu2021.hashnode.dev/a-simple-approach-for-background-task-in-django
    """

    task_id: Union[ str, None ] = None
    status: Status = Status.RUNNING
    value: Union[ int, None ] = None
    output : Union[ int, None ] = None

    # default constructor
    def __init__(self):
        self.task_id = str( uuid1() )
        cache.set( self.task_id, self, 3600 )

    def set( self,
        status : Status,
        value : int,
        progress_message : Union[ str, None ] = None) -> object:

        self.status = status.value
        self.value = value
        self.progress_message = progress_message

        cache.set( self.task_id, self, settings.WEBSCRAPER_CACHING_DURATION )

    def get_task_id( self ):
        return self.task_id

    def __str__(self):
        return f"{self.task_id} - {self.status} {self.value} {self.outputs}"

