from django.db.models import Q
from django.core.management.base import BaseCommand

from webscraping.models import Webscrape
from webscraping.modules.threader.classes.TaskDispatcher import TaskDispatcher
from webscraping.modules.threader.classes.TaskHandler import TaskHandler

from django_app import settings
import subprocess
import datetime

logger = settings.logger


class Command(BaseCommand):
    help = "Checks the task_todo field in Webscrape models and dispatches tasks."

    def handle(self, *args, **kwargs):
        """
            Main logic for the command.

            -----------
                With Deepseek / Python - 62610719, and prior
            -----------
        """

        # -------------------
        # Check tasks to end
        # -------------------
        taskDispatcher = TaskDispatcher(Webscrape)
        tasks = taskDispatcher.check_tasks_to_end()


        if not len(tasks):
            # Check for next tasks with Task handler
            # -------------------------------------
            taskHandler = TaskHandler.get_taskHandler(self.taskClass)
            i, n = taskHandler.start_next_tasks()

            msg = ""
            if i:
                msg = self.style.SUCCESS(
                    f"\n\n\t\t--------------------------------------------------------"
                    f"\n\t\t{i} task(s) started, {n} task(s) running..."
                    f"\n\t\t--------------------------------------------------------\n\n"
                )

            else:
                msg = self.style.INFO(
                    f"\n\n\t\t--------------------------------------------------------"
                    f"\n\t\t{0} task(s) started, {n} task(s) running..."
                    f"\n\t\t--------------------------------------------------------\n\n"
                )

            self.stdout.write(msg), logger.info(msg)

        exit()

