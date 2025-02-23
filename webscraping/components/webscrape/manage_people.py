_C='lastName'
_B='firstName'
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
class ManagePeopleView(UnicornView):
	'\n        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/\n    ';website_url:str='https://www.truthfinder.com';"\n        title: str = ''\n        firstName: str = 'David'\n        lastName: str = 'Jonathan'\n        middleName: str = 'Henry'\n        middleInitial: str = 'H.'\n        age: Union[ int, None ] = 51\n        city: str = 'Los Angeles'\n        state: str = 'CA'\n        country: str = 'USA'\n    ";title:str='';firstName:str='';lastName:str='';middleName:str='';middleInitial:str='';age:Union[int,_A]=_A;city:str='';state:str='';country:str='';task_name:str='truthfinder.sequences/find-person-in-usa-new.sequence.json';website_urls=_A;us_states=_A;countries=_A;by_list:str='';names_list:list=[];webscrape:Webscrape=_A;webscrapes:Union[QuerySetType[Webscrape],_A]=_A
	def setTitle(A,value):A.title=value
	def mount(A):A.website_urls=A.parent.website_urls;A.countries=A.parent.countries;A.us_states=A.parent.us_states
	def _exec(A,line,variables,i):
		C=variables;_print(f'\n            --------- EXECUTING ------------\n                name: "{C[_B]} {C[_C]}"...\n            --------------------------------\n            ',VERBOSITY=0);B=Webscrape(website_url=A.website_url,firstName=C[_B],lastName=C[_C],task_name=A.task_name)
		if i==0:B.by_list=A.by_list
		else:B.parent=A.webscrape
		B.task_variables=model_to_dict(A.webscrape);_print('-------------------------| %s'%B.task_variables,VERBOSITY=3);B=A.parent.set_queuable_task_queued(webscrape=B)
		if i==0:A.webscrape=B
	def scrape(B):
		'\n            __________________________________________________\n            1.   Split lines\n            2.   Start scrapes loop\n            2.1  First:\n                 - Create and assign main\n                 - Will hold by_text lines value\n                 - Append to webscrapes list\n            2.2  Others:\n                 - Assign 1st as parent\n                 - Append to main list\n            2.3  All → handled in Webscrape.update_ended_task_status():\n                 - Update corresponding line\n                 - Replace in main by_text\n                 - Save main → Updates ui textarea\n            __________________________________________________\n        ';D='✓'
		if not len(B.names_list):B.names_list=B.by_list.split('\n')
		E=0
		for A in B.names_list:
			if A:
				F=A.split(' ')[0];G=A.split(' ')[1];C={_B:F,_C:G}
				if A.find(D)<0 and A.find('✗')<0:B._exec(A,C,E);_print('\n                        ---------- PROCESSING ----------\n                            name: "%s" (Processing...)\n                        --------------------------------\n                        '%f"{C[_B]} {C[_C]}",VERBOSITY=0);E+=1
				else:_print('\n                        ---------- SKIPPING ------------\n                            name: "%s" (Processed %s)\n                        --------------------------------\n                        '%(f"{C[_B]} {C[_C]}",D if A.find(D)<0 else'✗'),VERBOSITY=0)
	def clear_fields(A):A.title='';A.firstName='';A.lastName='';A.middleName='';A.middleInitial='';A.age='';A.city='';A.state=''