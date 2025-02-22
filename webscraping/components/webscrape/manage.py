from django_unicorn.components import UnicornView, QuerySetType
from django.conf import settings
from django.forms.models import model_to_dict

from django_app.settings import _print
from webscraping.models import Webscrape

from datetime import date, datetime
from enum import Enum
from typing import Union
import copy

class MessageStatus(Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    NOTICE = "Notice"


class ManageView(UnicornView):
    """
        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/
    """
    webscrape: Webscrape = None


    website_url: str = 'https://www.truthfinder.com'
    """
        title: str = ''
        firstName: str = 'David'
        lastName: str = 'Jonathan'
        middleName: str = 'Henry'
        middleInitial: str = 'H.'
        age: Union[ int, None ] = 51
        city: str = 'Los Angeles'
        state: str = 'CA'
        country: str = 'USA'
    """

    title: str = ''
    firstName: str = ''
    lastName: str = ''
    middleName: str = ''
    middleInitial: str = ''
    age: Union[ int, None ] = None
    city: str = ''
    state: str = ''
    country: str = ''
    task_name: str = ''

    force_run: bool = False

    tasks: dict = {
        "truthfinder.com": "truthfinder.sequences/find-person-in-usa-new.sequence.json",
    }
    tasks_tuples: list[tuple] = [(
        "truthfinder.com", 
        "truthfinder.sequences/find-person-in-usa-new.sequence.json",
    )]

    website_urls = None
    us_states = None
    countries = None

    webscrapes: QuerySetType[Webscrape] = Webscrape.objects.all()

    def setTitle(self, value):
        self.title = value

    def mount(self):
        self.website_urls = self.parent.website_urls
        self.countries = self.parent.countries
        self.us_states = self.parent.us_states

        if settings.DEBUG:
            self.tasks = {
                "truthfinder.com": "truthfinder.sequences/find-person-in-usa-new.sequence.json",
                "localhost": "localhost-test.sequences/localhost-test.sequence.json",
                "localhost-fail": "localhost-test.sequences/localhost-test-fail.sequence.json",
            }
        
        self.tasks_tuples = []
        for key in self.tasks:
            self.tasks_tuples.append((key, self.tasks[key]))


    def scrape(self):
        """
            __________________________________________________
            Compute task name and task start url from user filled & chosen fields:
            
            Webscrape variables: (filled field)
            ------------------- 
                - first and last names
                - first and last names, state
                - first and last names, state, city
                - first and last names, state, city
               
            Webscrape site: (choice field)
            --------------
                - truthfinder.com
            __________________________________________________
        """        
        if not self.task_name:
            self.task_name = self.tasks[self.website_url],

        self.webscrape = Webscrape(
            website_url = self.website_url,
            title = self.title,
            firstName = self.firstName,
            lastName = self.lastName,
            middleName = self.middleName,
            middleInitial = self.middleInitial,
            age = self.age,
            city = self.city,
            state = self.state,

            task_name = self.task_name,
        )

        # Get task variables from user given + model fields
        self.webscrape.task_variables = model_to_dict(self.webscrape)
        _print(f'-------------------------| self.webscrape.task_name: {self.webscrape.task_name}', VERBOSITY=0)


        if self.force_run:
            # Force run and reload...
            # --------------------
            self.webscrape = self.parent.force_task_run(self.webscrape)
            self.parent.load_table()

        else:
            # If Queueable: set for scrape: set task status = QUEUED
            # ---------------------
            self.webscrape = self.parent.set_queuable_task_queued( 
                webscrape = self.webscrape
            )

            self.save()


    def save(self):
        self.webscrape.save()
        self.parent.load_table()


    def clear_fields(self):
        self.title = ''
        self.firstName = ''
        self.lastName = ''
        self.middleName = ''
        self.middleInitial = ''
        self.age = ''
        self.city = ''
        self.state = ''

        self.call('clear_fields')

