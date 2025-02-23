_A=None
from django_unicorn.components import UnicornView,QuerySetType
from django.conf import settings
from django.forms.models import model_to_dict
from django_app.settings import _print
from webscraping.modules.threader.classes.TaskHandler import TaskHandler
from webscraping.models import Webscrape
from webscraping.views import webscrape_steps_long_running_method
from datetime import date,datetime
from enum import Enum
from typing import Union
import copy
class MessageStatus(Enum):SUCCESS='Success';ERROR='Error';NOTICE='Notice'
class ManageCustomView(UnicornView):
	'\n        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/\n    ';webscrape:Webscrape=_A;website_url:str='';"\n        title: str = ''\n        firstName: str = 'David'\n        lastName: str = 'Jonathan'\n        middleName: str = 'Henry'\n        middleInitial: str = 'H.'\n        age: Union[ int, None ] = 51\n        city: str = 'Los Angeles'\n        state: str = 'CA'\n        country: str = 'USA'\n    ";title:str='';firstName:str='';lastName:str='';middleName:str='';middleInitial:str='';age:Union[int,_A]=_A;city:str='';state:str='';country:str='';task_name:str='';website_urls=_A;us_states=_A;countries=_A;new_media_base64=_A;new_media_file_name=_A;webscrapes:QuerySetType[Webscrape]=Webscrape.objects.all()
	def setTitle(A,value):A.title=value
	def set_task_variable(A,field_value):B=field_value;A.task_variables[B[0]]=B[1];_print('---------------| self.task_variables: %s'%A.task_variables,VERBOSITY=3)
	def mount(A):
		A.website_urls=A.parent.website_urls;A.countries=A.parent.countries;A.us_states=A.parent.us_states;A.webscrape_tasks=A.parent.webscrape_tasks;_print('---------------| self.webscrape_tasks: %s'%A.webscrape_tasks,VERBOSITY=3)
		if settings.DEBUG:0
	def scrape(A):'\n            __________________________________________________\n            Compute task name and task start url from user filled & chosen fields:\n            \n            Webscrape variables: (filled field)\n            ------------------- \n                - first and last names\n                - first and last names, state\n                - first and last names, state, city\n                - first and last names, state, city\n               \n            Webscrape site: (choice field)\n            --------------\n                - truthfinder.com\n            __________________________________________________\n        ';A.webscrape=Webscrape(website_url=A.website_url,title=A.title,firstName=A.firstName,lastName=A.lastName,middleName=A.middleName,middleInitial=A.middleInitial,age=A.age,city=A.city,state=A.state,task_name=A.task_name);A.webscrape.task_variables=model_to_dict(A.webscrape);_print('-------------------------| %s'%A.webscrape.task_variables,VERBOSITY=3);A.webscrape=A.parent.set_queuable_task_queued(webscrape=A.webscrape);A.save()
	def save(A):A.webscrape.save();A.clear_fields();return A.parent.load_table(force_render=True)
	def clear_fields(A):A.title='';A.firstName='';A.lastName='';A.middleName='';A.middleInitial='';A.age='';A.city='';A.state=''