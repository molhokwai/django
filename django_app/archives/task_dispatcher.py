from webscraping.models import (
    Webscrape, TaskHandler
)
from webscraping.views import webscrape_steps_long_running_method
from django.core.cache import cache


def task_dispatch(task_name: str, webscrape: Webscrape):
    """
    Dispatches tasks based on the task_name.

    Args:
        task_name (str): The name of the task to execute.
        webscrape (Webscrape): The Webscrape instance associated with the task.
    """
    method = {
        "webscrape_steps_long_running_method": webscrape_steps_long_running_method
    }.get(task_name, ValueError(f"Unknown task: {task_name}"))

    # Task handler from cache
    # ------------------------
    key = TaskHandler.get_self_cache_key()
    taskHandler = cache.get( key )
    if not taskHandler:
        taskHandler = TaskHandler()
        cache.set( key, taskHandler )

    # Queue task with Task handler
    # -----------------------------
    taskHandler.queue_task( method, [ webscrape ] )

    return True

