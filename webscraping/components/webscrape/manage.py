from django_unicorn.components import UnicornView, QuerySetType
from django.conf import settings
from django.forms.models import model_to_dict

from datetime import date, datetime
from webscraping.models import Webscrape, TaskProgress, TaskHandler

from webscraping.views import webscrape_steps_long_running_method


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


    task_name: str = "truthfinder.sequences/find-person-in-usa.sequence.json"

    us_states = None
    countries = None

    webscrapes: QuerySetType[Webscrape] = Webscrape.objects.all()

    def setTitle(self, value):
        self.title = value

    def mount(self):
        self.countries = self.parent.countries
        self.us_states = self.parent.us_states


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
        print('-------------------------| ', self.webscrape.task_variables)

        # Get/Generate task id with Task handler
        self.parent.taskHandler.queue_task(
            webscrape_steps_long_running_method, [ self.webscrape ] )

        self.save()


    def save(self):
        self.webscrape.save()
        self.clear_fields()
        return self.parent.load_table(force_render=True)


    def update_list(self):
        self.parent.load_table(force_render=True)


    def clear_fields(self):
        self.title = ''
        self.firstName = ''
        self.lastName = ''
        self.middleName = ''
        self.middleInitial = ''
        self.age = ''
        self.city = ''
        self.state = ''


