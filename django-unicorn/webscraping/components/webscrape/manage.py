from django_unicorn.components import UnicornView, QuerySetType
from django.conf import settings

from datetime import date, datetime
from webscraping.models import Webscrape


from .webscrapes import MessageStatus


class ManageView(UnicornView):
    """
        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/
    """
    webscrape: Webscrape = None


    website_url: str = ''
    title: str = ''
    first_name: str = ''
    last_name: str = ''
    middle_name: str = ''
    middle_initials: str = ''
    age: int = None
    city: str = ''
    state: str = ''
    country: str = '' 

    us_states = None
    countries = None

    new_media_base64 = None
    new_media_file_name = None

    webscrapes: QuerySetType[Webscrape] = Webscrape.objects.all()

    def setTitle(self, value):
        self.title = value

    def mount(self):
        self.countries = self.parent.countries
        self.us_states = self.parent.us_states

        # For testing...
        # --------------
        if settings.DEBUG:
            self.webscrape = Webscrape.objects.first()


    def add(self):

        print('------------------ | ----------------', str(self.title), str(self.age))
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
        )
        self.clear_fields()
        return self.parent.load_table(force_render=True)

    def scrape(self):
        self.add()


    def update_list(self):
        self.parent.load_table(force_render=True)


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


