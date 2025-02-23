from django.db.models import Q
from django.core.management.base import BaseCommand
from webscraping.models import Webscrape
from webscraping.modules.threader.classes.TaskDispatcher import TaskDispatcher
from webscraping.modules.threader.classes.TaskHandler import TaskHandler
from django_app import settings
import subprocess,datetime
logger=settings.logger
class Command(BaseCommand):
	help='Calls TaskHandler to dequeue and run the queued Webscrape models tasks...'
	def handle(B,*H,**I):
		'\n            Main logic for the command.\n\n            -----------\n                With Deepseek / Python - 62610719, and prior\n            -----------\n\n            # cron commands\n            # The cron commands to be set: scripts run, and intervalled scripts kill/clear\n            # to flush loose running processes and threads\n            # ---------------------------------------------------------------------------\n\n            */2 * * * * ~/@webscraper/django_app/management/scripts/webscraping-cron-exec-tasks-to-queue\n            */2 * * * * ~/@webscraper/django_app/management/scripts/webscraping-cron-exec-dequeue-and-run-tasks\n            */2 * * * * ~/@webscraper/django_app/management/scripts/webscraping-cron-exec-tasks-to-update\n            */5 * * * * ~/@webscraper/django_app/management/scripts/webscraping-cron-exec-tasks-to-end\n            */10 * * * * pkill -f "check_tasks"\n            */10 * * * * pkill -f "webscraping-cron-exec"\n            */10 * * * * pkill -f "marionette"\n            */10 * * * * pkill -f "dequeue_and_run"\n\n        '
		try:E=subprocess.run(['ps','-eF'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);C=len([A for A in E.stdout.splitlines()if'marionette'in A.lower()])
		except Exception as F:A=B.style.ERROR(f"-----| django webscraper - ./management | Error counting threads: {F}");B.stdout.write(A),logger.debug(A);return
		if C>=settings.WEBSCRAPER_THREADS_MAX:A=B.style.WARNING(f"""

\t\t--------------------------------------------------------
\t\tThread limit reached ({C}/{settings.WEBSCRAPER_THREADS_MAX}). Skipping task dispatch.
\t\t--------------------------------------------------------

""");B.stdout.write(A),logger.info(A);return
		G=TaskDispatcher(Webscrape);D=G.dequeue_and_run();A=''
		if D:A=B.style.SUCCESS(f"""

\t\t--------------------------------------------------------
\t\t{len(D)} task(s) dequeued...
\t\t--------------------------------------------------------

""")
		else:A=B.style.NOTICE(f"""

\t\t--------------------------------------------------------
\t\t{0} task(s) dequeued...
\t\t--------------------------------------------------------

""")
		B.stdout.write(A),logger.info(A);exit()