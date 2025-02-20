from django.db.models import Q
from django_unicorn.components import LocationUpdate, UnicornView, QuerySetType
from django.shortcuts import redirect

from django_app.settings import _print, logger

from webscraping.models import (
    Webscrape, WebscrapeTasks, WebsiteUrls,
    Countries, USStates,
    StatusTextChoices
)
from webscraping.modules.threader.classes.TaskProgress import Status


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

    excluded_fields = ('id', 'title', 'task_run_id', 'task_name', 'task_variables', 'task_todo',
                       'task_attempts', 'middleInitial', 'middleName', 'country', 'by_list',
                       'task_queue', 'parent', 'webscrape_children')
    sort_fields = ('task_progress', 'task_status', 'created_on', 'last_modified')

    default_sort: str = "-created_on"

    # tables value types: Union[ QuerySetType[Webscrape], None ]
    # ---------------------------------------------------
    statuses = StatusTextChoices.values
    tables = []
    default_webscrape_status = "RUNNING"


    def mount(self):
        if self.parent:
            self.us_states = self.parent.us_states
            self.countries = self.parent.countries

        self.fields = [f.name for f in Webscrape._meta.get_fields()]
        self.table_fields = copy.copy(self.fields)
        for val in self.excluded_fields:
            self.table_fields.remove(val)

        self.load_table()


    _sort: str = None
    def get_sort(self, field: str = None):
        if field:
            sign = -1
            if self._sort:
                if field == self._sort[1:]:
                    # The current sort field is sent for reversing:
                    # Get and invert sign
                    # -----------------------------
                    sign = int(self._sort[:1]) * -1

            sign_str = "-" if sign == -1 else "+"
            self._sort = f"{sign_str}{field}"

        elif not self._sort:
            self._sort = self.default_sort

        return self._sort

    def sort(self, query_string: str):
        """
            Sorts the corresponding table, using querystring to identify which.

            query_string
                A url parameters like query string variables,
                Workaround to bypass Unicorn multiple arguments js call issue...
                @ToDo :: Fix in Unicorn framework (branch?)

                From javascript:
                    ```js
                        //* Convert object to query string
                        const params = { _response, think };
                        const queryString = new URLSearchParams(params).toString();
                    ```
        """

        # Convert query string back to dictionary
        # ---------------------------------------
        parsed_dict = None
        if query_string:
            parsed_dict = {k: v[0] \
                    for k, v in parse_qs(query_string).items()}

        self.load_table(
            status = parsed_dict["status"],
            sort_field = parsed_dict["field"]
        )



    def load_table(self,
                   force_render=False,
                   status: str = None,
                   sort_field: str = None):
        """
            Description
                ...
                Sort happens entirely backend view side, 
                the frontend only sends the field

            Args
                force_render: bool
                table: str
                sort: str
        """
        sort = self.get_sort(field=sort_field)

        if not (status and sort_field):

            # self.webscrapes = Webscrape.objects.filter(Q(parent__isnull=True)).order_by("-last_modified")
            # ---------------------------
            self.webscrapes = Webscrape.objects.filter(
                    Q(created_on__gt=datetime.datetime(2025,2,11))
            )

            # Start scrape task for webscrape for which not done yet
            # ---------------------------
            for webscrape in self.webscrapes:
                if not webscrape.task_attempts:
                    webscrape.task_attempts = 0
                    webscrape.save()

                if self.parent:
                    self.parent.set_queuable_task_queued(webscrape = webscrape)


            # Update webscrape tasks status
            # ---------------------------
            i = len(self.webscrapes) - 1
            while i >= 0:
                self.webscrapes[i].update_ended_task_status()
                i -= 1

            # webscrapes tables by status
            # ---------------------------
            self.tables = list(map(lambda status: \
                    (
                        status,
                        self.webscrapes.filter(
                            Q(task_status=status)
                        ).order_by(sort)[:20]
                    ),
                    self.statuses
                )
            )

        else:
            # webscrape table by status
            # --------------------------
            i = self.statuses.index(status)
            self.tables[i] = (
                status,
                self.webscrapes.filter(
                    Q(task_status=status)
                ).order_by(sort)[:20]
            )


        # if len(self.webscrapes):
        #     self.webscrapes = self.webscrapes[0:10]
        # ---------------------------
        self.force_render = force_render


    def reload(self):
        return redirect('webscrape')


    def messages_display(self, status:MessageStatus=None, message:str=""):
        if status == MessageStatus.SUCCESS:
            messages.success(self.request, message)
        elif status  == MessageStatus.ERROR:
            messages.error(self.request, message)
