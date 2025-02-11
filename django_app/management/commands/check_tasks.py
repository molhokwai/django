from django.db.models import Q
from django.core.management.base import BaseCommand
from webscraping.models import Webscrape
from django_app.task_dispatcher import task_dispatch

import datetime


class Command(BaseCommand):
    help = "Checks the task_todo field in Webscrape models and dispatches tasks."

    def handle(self, *args, **kwargs):
        """
            Main logic for the command.
        """

        # Fetch Webscrape objects where task_todo is not null
        # ---------------------------------------------------
        tasks = Webscrape.objects.filter(
            Q(task_todo__isnull=False)
            & Q(created_on__gt=datetime.datetime(2025,2,11))
        )

        for task in tasks:
            # Dispatch the task based on the value of task_todo
            # -------------------------------------------------
            task_dispatch(task.task_todo, task)

            # Clear the task_todo field after dispatching
            # -------------------------------------------
            task.task_todo = None
            task.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"\n\n\t\t--------------------------------------------------------"
                f"\n\t\tTask checking and dispatching completed: {str(len(tasks))} tasks done."
                f"\n\t\t--------------------------------------------------------\n\n"))

