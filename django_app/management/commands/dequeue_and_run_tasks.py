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
    help = "Calls TaskHandler to dequeue and run the queued Webscrape models tasks..."

    def handle(self, *args, **kwargs):
        """
            Main logic for the command.

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

        # --------------------------------------------------
        # Count the number of running "marionette" processes
        # --------------------------------------------------
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

        # --------------------------------------------------
        # Check if the number of running threads exceeds the maximum allowed
        # --------------------------------------------------
        if running_threads >= settings.WEBSCRAPER_THREADS_MAX:
            msg = self.style.WARNING(
                f"\n\n\t\t--------------------------------------------------------"
                f"\n\t\tThread limit reached ({running_threads}/{settings.WEBSCRAPER_THREADS_MAX}). Skipping task dispatch."
                f"\n\t\t--------------------------------------------------------\n\n"
            )
            self.stdout.write(msg), logger.info(msg)
            return

        # -------------------
        # Dequeue and run tasks
        # -------------------
        taskDispatcher = TaskDispatcher(Webscrape)
        tasks = taskDispatcher.dequeue_and_run()

        msg = ""
        if tasks:

            msg = self.style.SUCCESS(
                f"\n\n\t\t--------------------------------------------------------"
                f"\n\t\t{len(tasks)} task(s) dequeued..."
                f"\n\t\t--------------------------------------------------------\n\n"
            )

        else:

            msg = self.style.NOTICE(
                f"\n\n\t\t--------------------------------------------------------"
                f"\n\t\t{0} task(s) dequeued..."
                f"\n\t\t--------------------------------------------------------\n\n"
            )

        self.stdout.write(msg), logger.info(msg)

        exit()

