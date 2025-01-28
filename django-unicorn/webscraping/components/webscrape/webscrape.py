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


class WebscrapeView(UnicornView):
    webscrapes = Webscrape.objects.none()
    us_states = None
    countries = None
    fields = None
    table_fields = None

    excluded_fields = ('id', 'title', 'task_id', 'task_name', 'task_variables', 'middleInitial', 'middleName', 'country', 'created_on', 'last_modified')


    def mount(self):
        self.us_states = list(zip(USStates.values, USStates.names))
        self.countries = list(zip(Countries.values, Countries.names))

        self.fields = [f.name for f in Webscrape._meta.get_fields()]
        self.table_fields = copy.copy(self.fields)
        for val in self.excluded_fields:
            self.table_fields.remove(val)

        self.load_table()


    def load_table(self, webscrape: Webscrape = None, force_render=False):
        self.webscrapes = Webscrape.objects.all().order_by("-last_modified")
        if len(self.webscrapes):
            self.webscrapes = self.webscrapes[0:10]
        self.force_render = force_render


    def reload(self):
        return redirect('webscrape')



    def get_task_by_task_id(self, task_id):
        return Webscrape.objects.get(task_id=task_id)


    def get_task_progress_by_task_id(self, task_id):
        webscrape = self.get_task_by_task_id(task_id)
        return webscrape.task_progress


    def get_task_outputs_by_task_id(self, task_id):
        webscrape = self.get_task_by_task_id(task_id)
        return webscrape.task_outputs


    def messages_display(self, status:MessageStatus=None, message:str=""):
        if status == MessageStatus.SUCCESS:
            messages.success(self.request, message)
        elif status  == MessageStatus.ERROR:
            messages.error(self.request, message)


    def add_count(self):
        messages.success(self.request, "| %i webscrapes loaded..." % len(self.webscrapes))
