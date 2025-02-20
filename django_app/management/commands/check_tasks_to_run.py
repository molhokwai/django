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
        # Count the number of running "marionette" processes
        try:
            result = subprocess.run(
                ["ps", "-eF"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            running_threads = len([line for line in result.stdout.splitlines() if "marionette" in line.lower()])
        except Exception as e:
            msg = self.style.ERROR(f"-----| django webscraper - ./management | Error counting threads: {e}")
            self.stdout.write(msg), logger.debug(msg)
            return

        # Check if the number of running threads exceeds the maximum allowed
        if running_threads >= settings.WEBSCRAPER_THREADS_MAX:
            msg = self.style.WARNING(
                f"\n\n\t\t--------------------------------------------------------"
                f"\n\t\tThread limit reached ({running_threads}/{settings.WEBSCRAPER_THREADS_MAX}). Skipping task dispatch."
                f"\n\t\t--------------------------------------------------------\n\n"
            )
            self.stdout.write(msg), logger.info(msg)
            return


        # -------------------
        # Check tasks to run
        # -------------------
        taskDispatcher = TaskDispatcher(Webscrape)
        tasks = taskDispatcher.check_tasks_to_run()


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
                msg = self.style.INFO(
                    f"\n\n\t\t--------------------------------------------------------"
                    f"\n\t\t{0} task(s) started, {n} task(s) running..."
                    f"\n\t\t--------------------------------------------------------\n\n"
                )

            self.stdout.write(msg), logger.info(msg)

        exit()

