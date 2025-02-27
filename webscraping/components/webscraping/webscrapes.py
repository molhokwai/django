from django_unicorn.components import LocationUpdate, UnicornView, QuerySetType
from django.shortcuts import redirect
from django.contrib import messages
from webscraping.models import Webscrape, Countries, USStates

from enum import Enum
import copy

class MessageStatus(Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    NOTICE = "Notice"


class WebscrapesView(UnicornView):
    webscrapes = Webscrape.objects.none()
    us_states = None
    countries = None
    fields = None
    table_fields = None


    def mount(self):
        self.us_states = list(zip(USStates.values, USStates.names))
        self.countries = list(zip(Countries.values, Countries.names))

        self.fields = [f.name for f in Webscrape._meta.get_fields()]
        self.table_fields = copy.copy(self.fields)
        # for val in ('id', 'middle_initials', 'country', 'created_on', 'last_modified'):
        for val in self.fields:
            if val not in ('website_url', 'firstName', 'lastName', 'age', 'city', 'state'):
                self.table_fields.remove(val)
        self.load_table()


    def load_table(self, force_render=False):
        self.webscrapes = Webscrape.objects.all().order_by("-created_on")
        # if len(self.webscrapes):
        #     self.webscrapes = self.webscrapes[0:100]
        self.force_render = force_render


    def reload(self):
        return redirect('webscraping')


    def messages_display(self, status:MessageStatus=None, message:str=""):
        if status == MessageStatus.SUCCESS:
            messages.success(self.request, message)
        elif status  == MessageStatus.ERROR:
            messages.error(self.request, message)


    def add_count(self):
        messages.success(self.request, "| %i webscrapes loaded..." % len(self.webscrapes))

