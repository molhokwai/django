from django_unicorn.components import UnicornView
from django.shortcuts import redirect
from django.contrib import messages

from webscraping.views import (
    parse_raw_outputs
)

from enum import Enum



class MessageStatus(Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    NOTICE = "Notice"


class WebscrapeDataView(UnicornView):
    aggregated_results = []
    aggregated_results_table_fields = [ 
        "NAME", "AGE", "LOCATION", "POSSIBLE_RELATIVES",
        "VERIFIED", "CRIMINAL_RECORDS" 
    ]



    def mount(self):
        self.aggregated_results = parse_raw_outputs()

        self.load_table()


    def load_table(self, force_render=False):
        self.force_render = force_render


    def reload(self):
        return redirect('webscrape_data')


    def messages_display(self, status:MessageStatus=None, message:str=""):
        if status == MessageStatus.SUCCESS:
            messages.success(self.request, message)
        elif status  == MessageStatus.ERROR:
            messages.error(self.request, message)
