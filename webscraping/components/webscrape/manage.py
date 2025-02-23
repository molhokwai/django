_C='truthfinder.sequences/find-person-in-usa-new.sequence.json'
_B='truthfinder.com'
_A=None
from django_unicorn.components import UnicornView,QuerySetType
from django.conf import settings
from django.forms.models import model_to_dict
from django_app.settings import _print
from webscraping.models import Webscrape
from datetime import date,datetime
from enum import Enum
from typing import Union
import copy
class MessageStatus(Enum):SUCCESS='Success';ERROR='Error';NOTICE='Notice'
class ManageView(UnicornView):
	'\n        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/\n    ';webscrape:Webscrape=_A;website_url:str='https://www.truthfinder.com';"\n        title: str = ''\n        firstName: str = 'David'\n        lastName: str = 'Jonathan'\n        middleName: str = 'Henry'\n        middleInitial: str = 'H.'\n        age: Union[ int, None ] = 51\n        city: str = 'Los Angeles'\n        state: str = 'CA'\n        country: str = 'USA'\n    ";title:str='';firstName:str='';lastName:str='';middleName:str='';middleInitial:str='';age:Union[int,_A]=_A;city:str='';state:str='';country:str='';task_name:str='';force_run:bool=False;tasks:dict={_B:_C};tasks_tuples:list[tuple]=[(_B,_C)];website_urls=_A;us_states=_A;countries=_A;webscrapes:QuerySetType[Webscrape]=Webscrape.objects.all()
	def setTitle(A,value):A.title=value
	def mount(A):
		A.website_urls=A.parent.website_urls;A.countries=A.parent.countries;A.us_states=A.parent.us_states
		if settings.DEBUG:A.tasks={_B:_C,'localhost':'localhost-test.sequences/localhost-test.sequence.json','localhost-fail':'localhost-test.sequences/localhost-test-fail.sequence.json'}
		A.tasks_tuples=[]
		for B in A.tasks:A.tasks_tuples.append((B,A.tasks[B]))
	def scrape(A):
		'\n            __________________________________________________\n            Compute task name and task start url from user filled & chosen fields:\n            \n            Webscrape variables: (filled field)\n            ------------------- \n                - first and last names\n                - first and last names, state\n                - first and last names, state, city\n                - first and last names, state, city\n               \n            Webscrape site: (choice field)\n            --------------\n                - truthfinder.com\n            __________________________________________________\n        '
		if not A.task_name:A.task_name=A.tasks[A.website_url],
		A.webscrape=Webscrape(website_url=A.website_url,title=A.title,firstName=A.firstName,lastName=A.lastName,middleName=A.middleName,middleInitial=A.middleInitial,age=A.age,city=A.city,state=A.state,task_name=A.task_name);A.webscrape.task_variables=model_to_dict(A.webscrape);_print(f"-------------------------| self.webscrape.task_name: {A.webscrape.task_name}",VERBOSITY=0)
		if A.force_run:A.webscrape=A.parent.force_task_run(A.webscrape);A.parent.load_table()
		else:A.webscrape=A.parent.set_queuable_task_queued(webscrape=A.webscrape);A.save()
	def save(A):A.webscrape.save();A.parent.load_table()
	def clear_fields(A):A.title='';A.firstName='';A.lastName='';A.middleName='';A.middleInitial='';A.age='';A.city='';A.state='';A.call('clear_fields')