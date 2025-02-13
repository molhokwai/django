from django.db.models import Q
from django_unicorn.components import LocationUpdate, UnicornView, QuerySetType
from django.shortcuts import redirect

from django_app.settings import _print, WEBSCRAPER_TASK_MAX_ATTEMPTS

from webscraping.models import (
    Webscrape, WebscrapeTasks, WebsiteUrls,
    Countries, USStates,
    Status
)

from enum import Enum
from typing import Union
import copy, datetime



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

    excluded_fields = ('id', 'title', 'task_id', 'task_name', 'task_variables', 'task_todo', 'task_attempts',
                       'middleInitial', 'middleName', 'country', 'by_list', 'task_queue',
                       'last_modified', 'parent', 'webscrape_children')


    def mount(self):
        if self.parent:
            self.us_states = self.parent.us_states
            self.countries = self.parent.countries

        self.fields = [f.name for f in Webscrape._meta.get_fields()]
        self.table_fields = copy.copy(self.fields)
        for val in self.excluded_fields:
            self.table_fields.remove(val)

        self.load_table()


    def load_table(self, force_render=False):
        # self.webscrapes = Webscrape.objects.filter(Q(parent__isnull=True)).order_by("-last_modified")
        self.webscrapes = Webscrape.objects.filter(
                Q(created_on__gt=datetime.datetime(2025,2,11))
        ).order_by("-created_on")[:20]

        # Start scrape task for webscrape for which not done yet
        if False: # Debugging, cancelled...
            for webscrape in self.webscrapes:
                if not webscrape.task_attempts:
                    webscrape.task_attempts = 0
                    webscrape.save()

                if webscrape.task_status != Status.SUCCESS.value and not webscrape.task_id:
                    if webscrape.task_attempts < WEBSCRAPER_TASK_MAX_ATTEMPTS:
                        self.parent.queue_task(webscrape = webscrape)
                        _print('-------------------------| START >> '
                              'webscrape.webscrape→load_table: self.webscrapes: '
                              'task_status, attempts :: %s, %i - name :: %s' \
                              % (webscrape.task_status, webscrape.task_attempts,
                                f"{webscrape.firstName} {webscrape.lastName}"),
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
