from django_unicorn.components import UnicornView, QuerySetType
from django.conf import settings

from django_app.settings import _print
from webscraping.models import Webscrape


from datetime import date, datetime
from enum import Enum
import copy

class MessageStatus(Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    NOTICE = "Notice"


class ManageReverseView(UnicornView):
    """
        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/
    """
    webscrape: Webscrape = None


    website_url: str = 'https://www.truthfinder.com'
    title: str = ''
    first_name: str = ''
    last_name: str = ''
    middle_name: str = ''
    middle_initials: str = ''
    age: int = None
    city: str = ''
    state: str = ''
    country: str = ''

    task_name: str = ''
    task_variables: dict = ''
    task_id: int = None
    task_progress: int = None

    website_urls = None
    us_states = None
    countries = None

    new_media_base64 = None
    new_media_file_name = None

    webscrapes: QuerySetType[Webscrape] = Webscrape.objects.all()

    def setTitle(self, value):
        self.title = value

    def mount(self):
        self.website_urls = self.parent.website_urls
        self.countries = self.parent.countries
        self.us_states = self.parent.us_states

        # For testing...
        # --------------
        if settings.DEBUG:
            self.webscrape = Webscrape.objects.first()


    def add(self):

        _print(
            '------------------ | ----------------  %s - %s' \
            % str(self.title), str(self.age),
            VERBOSITY=3
        )
        Webscrape.objects.create(
            website_url = self.website_url,
            title = self.title,
            first_name = self.first_name,
            last_name = self.last_name,
            middle_name = self.middle_name,
            middle_initials = self.middle_initials,
            age = self.age,
            city = self.city,
            state = self.state,

            task_name = self.task_name,
            task_variables = self.task_variables,
            task_id = self.task_id
        )
        self.clear_fields()
        return self.parent.load_table(force_render=True)

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
        self.task_name = "..."

        # Get task variables from user given fields
        self.task_variables = "..."

        # Scrape: Start / Queue task
        webscrape = self.parent.queue_task( webscrape = webscrape )

        self.add()


    def clear_fields(self):
        self.title = ''
        self.first_name = ''
        self.last_name = ''
        self.middle_name = ''
        self.middle_initials = ''
        self.last_name = ''
        self.age = ''
        self.city = ''
        self.state = ''


