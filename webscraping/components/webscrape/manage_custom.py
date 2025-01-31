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


class ManageCustomView(UnicornView):
    """
        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/
    """
    webscrape: Webscrape = None


    website_url: str = ''
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


    task_name: str = ""

    us_states = None
    countries = None

    new_media_base64 = None
    new_media_file_name = None

    webscrapes: QuerySetType[Webscrape] = Webscrape.objects.all()

    def setTitle(self, value):
        self.title = value

    def set_task_variable(self, field_value: tuple):
        self.task_variables[field_value[0]] = field_value[1]
        print('---------------| self.task_variables: ', self.task_variables)

    def mount(self):
        self.countries = self.parent.countries
        self.us_states = self.parent.us_states
        self.webscrape_tasks = self.parent.webscrape_tasks       
        print('---------------| self.webscrape_tasks: ', self.webscrape_tasks)

        # For testing...
        # --------------
        if settings.DEBUG:
            # self.webscrape = Webscrape.objects.first()
            pass

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
        self.webscrape.task_id = TaskHandler().start_task(
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


