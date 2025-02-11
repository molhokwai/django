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


    task_name: str = "truthfinder.sequences/find-person-in-usa-new.sequence.json"

    website_urls = None
    us_states = None
    countries = None

    by_list: str = ''
    names_list: list = []

    webscrape: Webscrape = None
    webscrapes: Union[ QuerySetType[Webscrape], None ] = None


    def setTitle(self, value):
        self.title = value

    def mount(self):
        self.website_urls = self.parent.website_urls
        self.countries = self.parent.countries
        self.us_states = self.parent.us_states


    def _exec(self, line, variables, i):
        _print(
            f"""
            --------- EXECUTING ------------
                name: "{variables["firstName"]} {variables["lastName"]}"...
            --------------------------------
            """,
            VERBOSITY=0
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
        _print(
            '-------------------------| %s' % webscrape.task_variables,
            VERBOSITY=3
        )

        # Scrape: Start / Queue task
        webscrape = self.parent.queue_task( webscrape = webscrape )

        if i == 0:
            self.webscrape = webscrape



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
                _print(
                    """
                    ---------- PROCESSING ----------
                        name: "%s" (Processed %s)
                    --------------------------------
                    """ % (
                        f"{variables["firstName"]} {variables["lastName"]}",
                        "✓" if line.find("✓") < 0 else "✗"
                    ),
                    VERBOSITY=0
                )
                i += 1
            else:
                _print(
                    """
                    ---------- SKIPPING ------------
                        name: "%s" (Processed %s)
                    --------------------------------
                    """ % (
                        f"{variables["firstName"]} {variables["lastName"]}",
                        "✓" if line.find("✓") < 0 else "✗"
                    ),
                    VERBOSITY=0
                )



    def clear_fields(self):
        self.title = ''
        self.firstName = ''
        self.lastName = ''
        self.middleName = ''
        self.middleInitial = ''
        self.age = ''
        self.city = ''
        self.state = ''


