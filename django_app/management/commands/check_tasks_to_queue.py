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
    help = "Calls TaskDispatcher to fetch and queue the queueable Webscrape models tasks..."

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

        # -------------------
        # Check tasks to queue
        # -------------------
        taskDispatcher = TaskDispatcher(Webscrape)
        tasks = taskDispatcher.check_tasks_to_queue()

        exit()

