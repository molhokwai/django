from django.db.models import Q
from django.core.management.base import BaseCommand
from webscraping.models import (
    Webscrape, TaskHandler
)
from django_app.task_dispatcher import task_dispatch
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

        # Fetch Webscrape objects where task_todo is not null
        tasks = Webscrape.objects.filter(
            Q(task_todo__isnull=False)
            & ~Q(task_status="SUCCESS")
            & ~Q(task_progress__gte=100)
            & Q(created_on__gt=datetime.datetime(2025, 2, 11))
        )

        if len(tasks):
            for task in tasks:
                # Dispatch the task based on the value of task_todo
                task_dispatch(task.task_todo, task)

                # Clear the task_todo field after dispatching
                task.task_todo = None
                task.save()

            msg = self.style.SUCCESS(
                f"\n\n\t\t--------------------------------------------------------"
                f"\n\t\tTask checking and dispatching completed: {len(tasks)} tasks done."
                f"\n\t\t--------------------------------------------------------\n\n"
            )
            self.stdout.write(msg), logger.info(msg)

        else:
            # Task handler from cache
            # ------------------------
            key = TaskHandler.get_self_cache_key()
            taskHandler = cache.get( key )
            if not taskHandler:
                taskHandler = TaskHandler()
                cache.set( key, taskHandler )

            # Check for next tasks with Task handler
            # -------------------------------------
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

