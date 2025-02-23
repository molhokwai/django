from django.db.models import Q
from django.core.management.base import BaseCommand
from webscraping.models import Webscrape
from webscraping.modules.threader.classes.TaskDispatcher import TaskDispatcher
from webscraping.modules.threader.classes.TaskHandler import TaskHandler
from django_app import settings
import subprocess,datetime
logger=settings.logger
class Command(BaseCommand):
	help='Calls TaskDispatcher to fetch and queue the queueable Webscrape models tasks...'
	def handle(B,*C,**D):'\n            Main logic for the command.\n\n            -----------\n                With Deepseek / Python - 62610719, and prior\n            -----------\n\n            # cron commands\n            # The cron commands to be set: scripts run, and intervalled scripts kill/clear\n            # to flush loose running processes and threads\n            # ---------------------------------------------------------------------------\n\n            */2 * * * * ~/@webscraper/django_app/management/scripts/webscraping-cron-exec-tasks-to-queue\n            */2 * * * * ~/@webscraper/django_app/management/scripts/webscraping-cron-exec-dequeue-and-run-tasks\n            */2 * * * * ~/@webscraper/django_app/management/scripts/webscraping-cron-exec-tasks-to-update\n            */5 * * * * ~/@webscraper/django_app/management/scripts/webscraping-cron-exec-tasks-to-end\n            */10 * * * * pkill -f "check_tasks"\n            */10 * * * * pkill -f "webscraping-cron-exec"\n            */10 * * * * pkill -f "marionette"\n            */10 * * * * pkill -f "dequeue_and_run"\n\n        ';A=TaskDispatcher(Webscrape);E=A.check_tasks_to_queue();exit()