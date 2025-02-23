_A=None
from django_unicorn.components import UnicornView,QuerySetType
from django.conf import settings
from django_app.settings import _print
from webscraping.models import Webscrape
from datetime import date,datetime
from enum import Enum
import copy
class MessageStatus(Enum):SUCCESS='Success';ERROR='Error';NOTICE='Notice'
class ManageReverseView(UnicornView):
	'\n        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/\n    ';webscrape:Webscrape=_A;website_url:str='https://www.truthfinder.com';title:str='';first_name:str='';last_name:str='';middle_name:str='';middle_initials:str='';age:int=_A;city:str='';state:str='';country:str='';task_name:str='';task_variables:dict='';task_run_id:int=_A;task_progress:int=_A;website_urls=_A;us_states=_A;countries=_A;new_media_base64=_A;new_media_file_name=_A;webscrapes:QuerySetType[Webscrape]=Webscrape.objects.all()
	def setTitle(A,value):A.title=value
	def mount(A):
		A.website_urls=A.parent.website_urls;A.countries=A.parent.countries;A.us_states=A.parent.us_states
		if settings.DEBUG:A.webscrape=Webscrape.objects.first()
	def add(A):_print('------------------ | ----------------  %s - %s'%str(A.title),str(A.age),VERBOSITY=3);Webscrape.objects.create(website_url=A.website_url,title=A.title,first_name=A.first_name,last_name=A.last_name,middle_name=A.middle_name,middle_initials=A.middle_initials,age=A.age,city=A.city,state=A.state,task_name=A.task_name,task_variables=A.task_variables,task_run_id=A.task_run_id);A.clear_fields();return A.parent.load_table(force_render=True)
	def scrape(A):'        \n            __________________________________________________\n            Compute task name and task start url from user filled & chosen fields:\n            \n            Webscrape variables: (filled field)\n            ------------------- \n                - first and last names\n                - first and last names, state\n                - first and last names, state, city\n                - first and last names, state, city\n               \n            Webscrape site: (choice field)\n            --------------\n                - truthfinder.com\n            __________________________________________________\n        ';B='...';A.task_name=B;A.task_variables=B;C=A.parent.set_queuable_task_queued(webscrape=C);A.add()
	def clear_fields(A):A.title='';A.first_name='';A.last_name='';A.middle_name='';A.middle_initials='';A.last_name='';A.age='';A.city='';A.state=''