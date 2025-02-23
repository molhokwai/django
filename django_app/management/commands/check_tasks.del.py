from django.db.models import Q
from django.core.management.base import BaseCommand
from webscraping.models import Webscrape,TaskHandler
from django_app.task_dispatcher import task_dispatch
from django_app import settings
import subprocess,datetime
logger=settings.logger
class Command(BaseCommand):
	help='Checks the task_todo field in Webscrape models and dispatches tasks.'
	def handle(B,*L,**M):
		'\n            Main logic for the command.\n\n            -----------\n                With Deepseek / Python - 62610719, and prior\n            -----------\n        '
		try:J=subprocess.run(['ps','-eF'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True);F=len([A for A in J.stdout.splitlines()if'marionette'in A.lower()])
		except Exception as K:A=B.style.ERROR(f"-----| django webscraper - ./management | Error counting threads: {K}");B.stdout.write(A),logger.debug(A);return
		if F>=settings.WEBSCRAPER_THREADS_MAX:A=B.style.WARNING(f"""

\t\t--------------------------------------------------------
\t\tThread limit reached ({F}/{settings.WEBSCRAPER_THREADS_MAX}). Skipping task dispatch.
\t\t--------------------------------------------------------

""");B.stdout.write(A),logger.info(A);return
		E=Webscrape.objects.filter(Q(task_todo__isnull=False)&~Q(task_status='SUCCESS')&~Q(task_progress__gte=100)&Q(created_on__gt=datetime.datetime(2025,2,11)))
		if len(E):
			for C in E:task_dispatch(C.task_todo,C);C.task_todo=None;C.save()
			A=B.style.SUCCESS(f"""

\t\t--------------------------------------------------------
\t\tTask checking and dispatching completed: {len(E)} tasks done.
\t\t--------------------------------------------------------

""");B.stdout.write(A),logger.info(A)
		else:
			G=TaskHandler.get_self_cache_key();D=cache.get(G)
			if not D:D=TaskHandler();cache.set(G,D)
			H,I=D.start_next_tasks();A=''
			if H:A=B.style.SUCCESS(f"""

\t\t--------------------------------------------------------
\t\t{H} task(s) started, {I} task(s) running...
\t\t--------------------------------------------------------

""")
			else:A=B.style.INFO(f"""

\t\t--------------------------------------------------------
\t\t{0} task(s) started, {I} task(s) running...
\t\t--------------------------------------------------------

""")
			B.stdout.write(A),logger.info(A)
		exit()