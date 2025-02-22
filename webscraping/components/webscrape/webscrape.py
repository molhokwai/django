from django.db.models import Q
from django.forms.models import model_to_dict

from django_unicorn.components import LocationUpdate, UnicornView, QuerySetType
from django.shortcuts import redirect
from django.contrib import messages

from django_app.settings import _print

from webscraping.modules.threader.classes.TaskHandler import TaskHandler
from webscraping.modules.threader.classes.TaskDispatcher import TaskDispatcher
from webscraping.modules.threader.classes.TaskProgress import Status
from webscraping.models import (
    Webscrape, WebscrapeData,
    WebscrapeTasks, WebscrapeTaskNameChoices,
    WebsiteUrls,
    Countries, USStates,
)

from webscraping.views import (
    parse_raw_outputs,
    webscrape_steps_long_running_method
)
from webscraping.components.webscrape.table import TableView

from enum import Enum
from typing import Union
import os, copy, random


from django.conf import settings



class MessageStatus(Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    NOTICE = "Notice"


class WebscrapeView(UnicornView):
    website_urls = None
    webscrape_tasks = None

    us_states = None
    countries = None

    previous_outputs = []

    aggregated_results = []
    aggregated_results_nr = None
    aggregated_results_table_fields = [ 
        "NAME", "AGE", "LOCATION", "POSSIBLE_RELATIVES",
        "VERIFIED", "CRIMINAL_RECORDS" 
    ]

    webscrape_data_id: int = None

    def mount(self):
        self.us_states = list(zip(USStates.values, USStates.names))
        self.countries = list(zip(Countries.values, Countries.names))


        self.website_urls = list(zip([WebsiteUrls.TRUTHFINDER.value], [WebsiteUrls.TRUTHFINDER.name]))
        if settings.DEBUG:
            self.website_urls = list(zip(WebsiteUrls.values, WebsiteUrls.names))
            self.tasks = {
                "truthfinder.com": "truthfinder.sequences/find-person-in-usa-new.sequence.json",
                "localhost": "localhost-test.sequences/localhost-test.sequence.json",
                "localhost-fail": "localhost-test.sequences/localhost-test-fail.sequence.json",
            }


        self.webscrape_tasks = list(zip(
            [WebscrapeTasks.TRUTHFINDER_USA_FIND_A_PERSON.value], 
            [WebscrapeTasks.TRUTHFINDER_USA_FIND_A_PERSON.name]
        ))
        if settings.DEBUG:
            self.webscrape_tasks = list(zip(WebscrapeTasks.values, WebscrapeTasks.names))


        self.previous_outputs = self.get_previous_outputs()

        self.aggregated_results = parse_raw_outputs()
        self.aggregated_results_nr = len(self.aggregated_results)
        WebscrapeData.periodic_save_aggregated_results(self.aggregated_results)
        self.webscrape_data_id = WebscrapeData.objects.first().id

        self.load_table()


    def load_table(self, 
                   webscrape: Webscrape = None,
                   force_render=False):

        for child in self.children:
            if str(child).find('TableView') >= 0:
                child.load_table()

        self.force_render = force_render


    def reload(self):
        return redirect('webscrape')



    def force_task_run(self, 
                    webscrape: Union[ Webscrape, None ]  = None) -> Webscrape:
        """
            Description
                Forces task run, queues scrape tak by Webscrape object or task°id
                setting it to force run 

            Args
                webscrape: Union[ Webscrape, None ]
                task_run_id: Union[ str, None ]
                One of thwo arguments must be provided

            Raises
                ValueError if none of the both arguments are provided

            Returns
                Webscrape
        """
        if webscrape:
            pass
        elif task_run_id:
            webscrape = Webscrape.objects.get(task_run_id=task_run_id)
        else:
            raise ValueError("webscraping:unicorn :: webscrape.WebscrapeView.set_queuable_task_queued: "
                             "One of <webscrape:Webscrape> or <task_run_id: str> must be provided...")

        webscrape.task_todo = WebscrapeTaskNameChoices.WEBSCRAPE_STEPS.value

        taskDispatcher = TaskDispatcher(Webscrape)
        taskDispatcher.dispatch(
            webscrape.task_todo,
            webscrape, 
            force_run = True
        )

        return webscrape



    def set_queuable_task_queued(self, 
                    webscrape: Union[ Webscrape, None ]  = None) -> Webscrape:
        """
            Description
                Starts/queues scrape tak by Webscrape object or task°id

            Args
                webscrape: Union[ Webscrape, None ]
                task_run_id: Union[ str, None ]
                One of thwo arguments must be provided

            Raises
                ValueError if none of the both arguments are provided

            Returns
                Webscrape
        """
        if webscrape:
            pass
        elif task_run_id:
            webscrape = Webscrape.objects.get(task_run_id=task_run_id)
        else:
            raise ValueError("webscraping:unicorn :: webscrape.WebscrapeView.set_queuable_task_queued: "
                             "One of <webscrape:Webscrape> or <task_run_id: str> must be provided...")

        if TaskHandler.task_is_queueable(webscrape):

            # Get task variables from user given + model fields
            # -------------------------------------------------
            if not webscrape.task_variables:
                webscrape.task_variables = model_to_dict(webscrape)

            # Set task to be picked and queued
            # --------------------------------
            webscrape.task_todo = WebscrapeTaskNameChoices.WEBSCRAPE_STEPS.value
            webscrape.task_status = Status.QUEUED.value
            webscrape.save()

        return webscrape

    def task_is_running(self, task_run_id: str) -> int:
        taskProgress = TaskHandler.get_taskProgress(task_run_id)
        if taskProgress:
            return True


    def get_task_progress_data(self, task_run_id: str) -> int:
        task_progress_value = 0
        task_output = []

        webscrape = Webscrape.objects.get(task_run_id = task_run_id)
        task_progress_value = webscrape.task_progress
        if webscrape.task_status == Status.SUCCESS.value:
            task_output = webscrape.task_output

        # -----------------
        # Handled in `check_tasks_to_end`
        # @ToDo: See if to be kept here for redundandy...
        # -----------------
        if webscrape.task_status in (Status.SUCCESS.value, Status.FAILED.value):
            self.taskHandler.end_task_start_next(
                webscrape.task_run_id,
                taskObject = webscrape,
                do_save = True
            )

        task_progress_data = {
            "task_progress_value": task_progress_value,
            "task_output": task_output
        }


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
                _print(
                    '---------------| webscraping/Unicorn.webscrape.webscape >'
                    ' get_previous_outputs :: Error : %s' % str(err), 
                    VERBOSITY=0
                )
        return l


    def messages_display(self, status:MessageStatus=None, message:str=""):
        if status == MessageStatus.SUCCESS:
            messages.success(self.request, message)
        elif status  == MessageStatus.ERROR:
            messages.error(self.request, message)


    def add_count(self):
        messages.success(self.request, "| %i webscrapes loaded..." % len(self.webscrapes))

