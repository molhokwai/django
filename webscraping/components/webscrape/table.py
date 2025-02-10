from django_unicorn.components import LocationUpdate, UnicornView, QuerySetType
from django.shortcuts import redirect

from django_app.settings import _print
from webscraping.models import (
    Webscrape, WebscrapeTasks, WebsiteUrls,
    Countries, USStates,
    Status
)

from enum import Enum
from typing import Union
import copy



class MessageStatus(Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    NOTICE = "Notice"


class TableView(UnicornView):
    webscrapes = Webscrape.objects.none()

    countries = None
    us_states = None

    fields = None
    table_fields = None

    excluded_fields = ('id', 'title', 'task_id', 'task_name', 'task_variables',
                       'middleInitial', 'middleName', 'country', 'by_list', 'task_queue',
                       'last_modified', 'parent', 'webscrape_children')



    def mount(self):
        self.us_states = self.parent.us_states
        self.countries = self.parent.countries

        self.fields = [f.name for f in Webscrape._meta.get_fields()]
        self.table_fields = copy.copy(self.fields)
        for val in self.excluded_fields:
            self.table_fields.remove(val)

        self.parent.children.append(self)
        self.load_table()


    def load_table(self, force_render=False):
        # self.webscrapes = Webscrape.objects.filter(Q(parent__isnull=True)).order_by("-last_modified")
        self.webscrapes = Webscrape.objects.all().order_by("-last_modified")

        # Start scrape task for webscrape for which not done yet
        if False: # Debugging, cancelled...
            for webscrape in self.webscrapes:
                if webscrape.task_status != Status.SUCCESS.value and not webscrape.task_id:
                    self.scrape_by(webscrape = webscrape)
                    _print('-------------------------| START >> '
                          'webscrape.webscrape→load_table: self.webscrapes: '
                          'task_status, task_id :: %s, %s' \
                          % (webscrape.task_status, webscrape.task_id), 
                          VERBOSITY=3
                    )

        # Update webscrape tasks status
        i = len(self.webscrapes) - 1
        while i >= 0:
            self.webscrapes[i].update_task_status()
            i -= 1

        # if len(self.webscrapes):
        #     self.webscrapes = self.webscrapes[0:10]
        self.force_render = force_render


    def reload(self):
        return redirect('webscrape')


    def messages_display(self, status:MessageStatus=None, message:str=""):
        if status == MessageStatus.SUCCESS:
            messages.success(self.request, message)
        elif status  == MessageStatus.ERROR:
            messages.error(self.request, message)
