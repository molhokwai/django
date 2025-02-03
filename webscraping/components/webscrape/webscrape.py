from django.db.models import Q

from django_unicorn.components import LocationUpdate, UnicornView, QuerySetType
from django.shortcuts import redirect
from django.contrib import messages
from webscraping.models import (
    Webscrape, WebscrapeTasks, WebsiteUrls,
    Countries, USStates,
    Status, TaskHandler
)

from webscraping.views import parse_raw_outputs

from enum import Enum
import os, copy, random


from django.conf import settings



class MessageStatus(Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    NOTICE = "Notice"


class WebscrapeView(UnicornView):
    webscrapes = Webscrape.objects.none()
    website_urls = None
    webscrape_tasks = None

    us_states = None
    countries = None
    fields = None
    table_fields = None

    excluded_fields = ('id', 'title', 'task_id', 'task_name', 'task_variables',
                       'middleInitial', 'middleName', 'country', 'created_on',
                       'last_modified', 'parent', 'webscrape_children')

    previous_outputs = []

    aggregated_results = []
    aggregated_results_table_fields = [ 
        "NAME", "AGE", "LOCATION", "POSSIBLE_RELATIVES",
        "VERIFIED", "CRIMINAL_RECORDS" 
    ]

    taskHandler: TaskHandler = None


    def __init__(self):
        self.taskHandler = TaskHandler()


    def mount(self):
        self.us_states = list(zip(USStates.values, USStates.names))
        self.countries = list(zip(Countries.values, Countries.names))
        self.website_urls = list(zip(WebsiteUrls.values, WebsiteUrls.names))
        self.webscrape_tasks = list(zip(WebscrapeTasks.values, WebscrapeTasks.names))

        self.fields = [f.name for f in Webscrape._meta.get_fields()]
        self.table_fields = copy.copy(self.fields)
        for val in self.excluded_fields:
            self.table_fields.remove(val)

        self.previous_outputs = self.get_previous_outputs()

        self.aggregated_results = parse_raw_outputs()

        self.load_table()


    def load_table(self, webscrape: Webscrape = None, force_render=False):
        # self.webscrapes = Webscrape.objects.filter(Q(parent__isnull=True)).order_by("-last_modified")
        self.webscrapes = Webscrape.objects.all().order_by("-last_modified")

        i = len(self.webscrapes) - 1
        while i >= 0:
            self.webscrapes[i].update_task_status()
            i -= 1

        # if len(self.webscrapes):
        #     self.webscrapes = self.webscrapes[0:10]
        self.force_render = force_render


    def reload(self):
        return redirect('webscrape')


    def task_is_running(self, task_id: str) -> int:
        taskProgress = TaskHandler.get_taskProgress(task_id)
        if taskProgress:
            return True


    def get_task_progress_data(self, task_id: str) -> int:
        task_progress_value = 0
        task_output = []

        webscrape = Webscrape.objects.get(task_id = task_id)
        task_progress_value = webscrape.task_progress
        if webscrape.task_status == Status.SUCCESS.value:
            task_output = webscrape.task_output

        if webscrape.task_status in (Status.SUCCESS.value, Status.FAILED.value):
            self.taskHandler.stop_task(webscrape.task_id)

        task_progress_data = {
            "task_progress_value": task_progress_value,
            "task_output": task_output
        }
        print('---------------| Unicorn.webscrape.webscrape > get_task_progress_data', task_progress_data)


        return task_progress_data


    def get_previous_outputs(self):
        def read_file(file):
            with open(file) as f:
                return f.read()

        output_dir = os.path.join(
            settings.BASE_DIR, settings.WEBSCRAPER_SOURCE_PATH, 'output'
        )
        files = list(filter(lambda x: x.endswith('.txt'), os.listdir(output_dir)))
        l = []
        for f in files:
            try:
                l.append(read_file(os.path.join(output_dir, f)))
            except Exception as err:
                print(
                    '---------------| webscraping/Unicorn.webscrape.webscape > get_previous_outputs :: Error : ', err)
        return l


    def messages_display(self, status:MessageStatus=None, message:str=""):
        if status == MessageStatus.SUCCESS:
            messages.success(self.request, message)
        elif status  == MessageStatus.ERROR:
            messages.error(self.request, message)


    def add_count(self):
        messages.success(self.request, "| %i webscrapes loaded..." % len(self.webscrapes))

