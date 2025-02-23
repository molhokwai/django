_B='webscraping:unicorn :: webscrape.WebscrapeView.set_queuable_task_queued: One of <webscrape:Webscrape> or <task_run_id: str> must be provided...'
_A=None
from django.db.models import Q
from django.forms.models import model_to_dict
from django_unicorn.components import LocationUpdate,UnicornView,QuerySetType
from django.shortcuts import redirect
from django.contrib import messages
from django_app.settings import _print
from webscraping.modules.threader.classes.TaskHandler import TaskHandler
from webscraping.modules.threader.classes.TaskDispatcher import TaskDispatcher
from webscraping.modules.threader.classes.TaskProgress import Status
from webscraping.models import Webscrape,WebscrapeData,WebscrapeTasks,WebscrapeTaskNameChoices,WebsiteUrls,Countries,USStates
from webscraping.views import parse_raw_outputs,webscrape_steps_long_running_method
from webscraping.components.webscrape.table import TableView
from enum import Enum
from typing import Union
import os,copy,random
from django.conf import settings
class MessageStatus(Enum):SUCCESS='Success';ERROR='Error';NOTICE='Notice'
class WebscrapeView(UnicornView):
	website_urls=_A;webscrape_tasks=_A;us_states=_A;countries=_A;previous_outputs=[];aggregated_results=[];aggregated_results_nr=_A;aggregated_results_table_fields=['NAME','AGE','LOCATION','POSSIBLE_RELATIVES','VERIFIED','CRIMINAL_RECORDS'];webscrape_data_id:int=_A
	def mount(A):
		A.us_states=list(zip(USStates.values,USStates.names));A.countries=list(zip(Countries.values,Countries.names));A.website_urls=list(zip([WebsiteUrls.TRUTHFINDER.value],[WebsiteUrls.TRUTHFINDER.name]))
		if settings.DEBUG:A.website_urls=list(zip(WebsiteUrls.values,WebsiteUrls.names));A.tasks={'truthfinder.com':'truthfinder.sequences/find-person-in-usa-new.sequence.json','localhost':'localhost-test.sequences/localhost-test.sequence.json','localhost-fail':'localhost-test.sequences/localhost-test-fail.sequence.json'}
		A.webscrape_tasks=list(zip([WebscrapeTasks.TRUTHFINDER_USA_FIND_A_PERSON.value],[WebscrapeTasks.TRUTHFINDER_USA_FIND_A_PERSON.name]))
		if settings.DEBUG:A.webscrape_tasks=list(zip(WebscrapeTasks.values,WebscrapeTasks.names))
		A.previous_outputs=A.get_previous_outputs();A.aggregated_results=parse_raw_outputs();A.aggregated_results_nr=len(A.aggregated_results);WebscrapeData.periodic_save_aggregated_results(A.aggregated_results);A.webscrape_data_id=WebscrapeData.objects.first().id;A.load_table()
	def load_table(A,webscrape=_A,force_render=False):
		for B in A.children:
			if str(B).find('TableView')>=0:B.load_table()
		A.force_render=force_render
	def reload(A):return redirect('webscrape')
	def force_task_run(C,webscrape=_A):
		'\n            Description\n                Forces task run, queues scrape tak by Webscrape object or task°id\n                setting it to force run \n\n            Args\n                webscrape: Union[ Webscrape, None ]\n                task_run_id: Union[ str, None ]\n                One of thwo arguments must be provided\n\n            Raises\n                ValueError if none of the both arguments are provided\n\n            Returns\n                Webscrape\n        ';A=webscrape
		if A:0
		elif task_run_id:A=Webscrape.objects.get(task_run_id=task_run_id)
		else:raise ValueError(_B)
		A.task_todo=WebscrapeTaskNameChoices.WEBSCRAPE_STEPS.value;B=TaskDispatcher(Webscrape);B.dispatch(A.task_todo,A,force_run=True);return A
	def set_queuable_task_queued(B,webscrape=_A):
		'\n            Description\n                Starts/queues scrape tak by Webscrape object or task°id\n\n            Args\n                webscrape: Union[ Webscrape, None ]\n                task_run_id: Union[ str, None ]\n                One of thwo arguments must be provided\n\n            Raises\n                ValueError if none of the both arguments are provided\n\n            Returns\n                Webscrape\n        ';A=webscrape
		if A:0
		elif task_run_id:A=Webscrape.objects.get(task_run_id=task_run_id)
		else:raise ValueError(_B)
		if TaskHandler.task_is_queueable(A):
			if not A.task_variables:A.task_variables=model_to_dict(A)
			A.task_todo=WebscrapeTaskNameChoices.WEBSCRAPE_STEPS.value;A.task_status=Status.QUEUED.value;A.save()
		return A
	def task_is_running(B,task_run_id):
		A=TaskHandler.get_taskProgress(task_run_id)
		if A:return True
	def get_task_progress_data(D,task_run_id):
		B=0;C=[];A=Webscrape.objects.get(task_run_id=task_run_id);B=A.task_progress
		if A.task_status==Status.SUCCESS.value:C=A.task_output
		if A.task_status in(Status.SUCCESS.value,Status.FAILED.value):D.taskHandler.end_task_start_next(A.task_run_id,taskObject=A,do_save=True)
		E={'task_progress_value':B,'task_output':C};return E
	def get_previous_outputs(G):
		def C(file):
			with open(file)as A:return A.read()
		A=os.path.join(settings.BASE_DIR,settings.WEBSCRAPER_SOURCE_PATH,'output');D=list(filter(lambda x:x.endswith('.txt'),os.listdir(A)));B=[]
		for E in D:
			try:B.append(C(os.path.join(A,E)))
			except Exception as F:_print('---------------| webscraping/Unicorn.webscrape.webscape > get_previous_outputs :: Error : %s'%str(F),VERBOSITY=0)
		return B
	def messages_display(A,status=_A,message=''):
		B=message;C=status
		if C==MessageStatus.SUCCESS:messages.success(A.request,B)
		elif C==MessageStatus.ERROR:messages.error(A.request,B)
	def add_count(A):messages.success(A.request,'| %i webscrapes loaded...'%len(A.webscrapes))