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


class ManagePeopleView(UnicornView):
    """
        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/
    """
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

    by_list: str = ''
    names_list: list = []

    webscrape: Webscrape = None
    webscrapes: Union[ QuerySetType[Webscrape], None ] = None


    def setTitle(self, value):
        self.title = value

    def mount(self):
        self.countries = self.parent.countries
        self.us_states = self.parent.us_states


    def _exec(self, line, variables, i):
        print(
            """
            --------- EXECUTING ------------
                name: "%s"...
            --------------------------------
            """ % str(variables)
        )

        webscrape = Webscrape(
            website_url = self.website_url,
            firstName = variables["firstName"],
            lastName = variables["lastName"],
            task_name = self.task_name,
        )

        if i == 0:
            webscrape.by_list = self.by_list
        else:
            webscrape.parent = self.webscrape


        # Get task variables from user given + model fields
        webscrape.task_variables = model_to_dict(self.webscrape)
        print('-------------------------| ', webscrape.task_variables)

        # Get/Generate task id with Task handler
        self.parent.taskHandler.queue_task(
            webscrape_steps_long_running_method, [ webscrape ] )

        if i == 0:
            self.webscrape = webscrape
            self.save()
        else:
            self.save_webscrape(webscrape)



    def scrape(self):
        """
            __________________________________________________
            1.   Split lines
            2.   Start scrapes loop
            2.1  First:
                 - Create and assign main
                 - Will hold by_text lines value
                 - Append to webscrapes list
            2.2  Others:
                 - Assign 1st as parent
                 - Append to main list
            2.3  All → handled in Webscrape.update_task_status():
                 - Update corresponding line
                 - Replace in main by_text
                 - Save main → Updates ui textarea
            __________________________________________________
        """        
        if not len(self.names_list):
            self.names_list = self.by_list.split("\n")

        i = 0
        for line in self.names_list:
            firstName = line.split(" ")[0]
            lastName = line.split(" ")[1]
            variables = {
                "firstName": firstName,
                "lastName": lastName,
            }

            if line.find("✓") < 0 and line.find("✗") < 0:
                self._exec(line, variables, i)
                i += 1
            else:
                print(
                    """
                    ---------- SKIPPING ------------
                        name: "%s" (Processed %s)
                    --------------------------------
                    """ % (
                        str(variables),
                        "✓" if line.find("✓") < 0 else "✗"
                     )
                )

        return self.parent.load_table(force_render=True)


    def save(self):
        self.webscrape.save()
        return self.parent.load_table(force_render=True)


    def save_webscrape(self, webscrape):
        webscrape.save()
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


