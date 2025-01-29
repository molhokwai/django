from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils.text import slugify

from django.core.cache import cache

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
    task_progress = models.IntegerField(max_length=3, default=0)
    task_outputs = models.TextField(null=True, blank=True)

    # identification
    # --------------
    firstName = models.CharField(max_length=200, null=False, blank=False)
    lastName = models.CharField(max_length=200, null=False, blank=False)
    middleName = models.CharField(max_length=200, null=True, blank=True)
    middleInitial = models.CharField(max_length=6, null=True, blank=True)
    age = models.IntegerField(max_length=3, null=True, blank=True)

    # location
    # --------
    city = models.CharField(null=True, blank=True, max_length=200)
    state = models.CharField(null=True, blank=True, max_length=2,  choices=USStates.choices)
    country = models.CharField(null=True, blank=True, max_length=2,  choices=Countries.choices, default="US")

    # crud datetimes
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)




class TaskHandler:

    def start_task(self, method, args):

        task_progress = TaskProgress()
        t = threading.Thread( target=method, args=[ *args, task_progress ] )
        t.setDaemon(True)
        t.start()

        return task_progress.get_task_id()

    @staticmethod
    def get_task_progress( task_id : str ):
        return cache.get( task_id )


class Status(Enum):
    STARTED = 'STARTED'
    RUNNING = 'RUNNING'
    SUCCESS = 'SUCCESS'

class TaskProgress:

    task_id = str

    # default constructor
    def __init__(self):
        self.task_id = str( uuid1() )
        cache.set( self.task_id, self, 3600 )

    def set( self,
        status : Enum,
        progress_message : Union[ str, None ] = None,
        output : dict = None ) -> object:

        self.status = status.value
        self.progress_message = progress_message
        self.output = output

        cache.set( self.task_id, self, 3600 )

    def get_task_id( self ):
        return self.task_id
