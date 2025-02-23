from django.db.models import Q
from django.core.management.base import BaseCommand

from webscraping.models import Webscrape
from webscraping.modules.threader.classes.TaskDispatcher import TaskDispatcher
from webscraping.modules.threader.classes.TaskHandler import TaskHandler

from django_app import settings
import subprocess


logger = settings.logger


class Command(BaseCommand):
    help = "Calls TaskDispatcher to fetch and end the Webscrape models tasks to be ended..."

    def handle(self, *args, **kwargs):
        """
            Main logic for the command.

            -------------------
            ! @ToDo :: Same method / processes: `check_tasks_to_end`,  `check_tasks_to_update`,
                        separated because the process hangs when calling for threads stop...
                        To refactor...
            -------------------


            -----------
                With Deepseek / Python - 62610719, and prior
            -----------

            # cron commands
            # The cron commands to be set: scripts run, and intervalled scripts kill/clear
            # to flush loose running processes and threads
            # ---------------------------------------------------------------------------

            */2 * * * * ~/@webscraper/django_app/management/scripts/webscraping-cron-exec-tasks-to-queue
            */2 * * * * ~/@webscraper/django_app/management/scripts/webscraping-cron-exec-dequeue-and-run-tasks
            */2 * * * * ~/@webscraper/django_app/management/scripts/webscraping-cron-exec-tasks-to-update
            */5 * * * * ~/@webscraper/django_app/management/scripts/webscraping-cron-exec-tasks-to-end
            */10 * * * * pkill -f "check_tasks"
            */10 * * * * pkill -f "webscraping-cron-exec"
            */10 * * * * pkill -f "marionette"
            */10 * * * * pkill -f "dequeue_and_run"

        """

        # -------------------
        # Check tasks to end
        # -------------------
        taskDispatcher = TaskDispatcher(Webscrape)
        tasks = taskDispatcher.check_tasks_to_end("end")


        if not len(tasks):
            # Check for next tasks with Task handler
            # -------------------------------------
            taskHandler = TaskHandler.get_taskHandler(Webscrape)
            i, n = taskHandler.start_next_tasks()

            msg = ""
            if i:
                msg = self.style.SUCCESS(
                    f"\n\n\t\t--------------------------------------------------------"
                    f"\n\t\t{i} task(s) started, {n} task(s) running..."
                    f"\n\t\t--------------------------------------------------------\n\n"
                )

            else:
                msg = self.style.NOTICE(
                    f"\n\n\t\t--------------------------------------------------------"
                    f"\n\t\t{0} task(s) started, {n} task(s) running..."
                    f"\n\t\t--------------------------------------------------------\n\n"
                )

            self.stdout.write(msg), logger.info(msg)

        exit()

