from webscraping.models import Webscrape,TaskHandler
from webscraping.views import webscrape_steps_long_running_method
from django.core.cache import cache
def task_dispatch(task_name,webscrape):
	'\n    Dispatches tasks based on the task_name.\n\n    Args:\n        task_name (str): The name of the task to execute.\n        webscrape (Webscrape): The Webscrape instance associated with the task.\n    ';B=task_name;D={'webscrape_steps_long_running_method':webscrape_steps_long_running_method}.get(B,ValueError(f"Unknown task: {B}"));C=TaskHandler.get_self_cache_key();A=cache.get(C)
	if not A:A=TaskHandler();cache.set(C,A)
	A.queue_task(D,[webscrape]);return True