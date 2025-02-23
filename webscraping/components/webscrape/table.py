_A=None
from django.db.models import Q
from django.utils import timezone
from django_unicorn.components import LocationUpdate,UnicornView,QuerySetType
from django.shortcuts import redirect
from django_app.settings import _print,logger
from webscraping.models import Webscrape,WebscrapeTasks,WebsiteUrls,Countries,USStates,StatusTextChoices
from webscraping.modules.threader.classes.TaskProgress import Status
from enum import Enum
from typing import Union
import copy,datetime
from datetime import timedelta
class MessageStatus(Enum):SUCCESS='Success';ERROR='Error';NOTICE='Notice'
class TableView(UnicornView):
	webscrapes=Webscrape.objects.none();countries=_A;us_states=_A;fields=_A;table_fields=_A;excluded_fields='id','title','task_run_id','task_name','task_variables','task_todo','task_attempts','middleInitial','middleName','country','by_list','task_title','task_thread_started_at','task_thread_stopped_at','task_queue','parent','webscrape_children';sort_fields='task_progress','task_status','created_on','last_modified';default_sort:str='-created_on';statuses=StatusTextChoices.values;tables=[];default_webscrape_status='RUNNING'
	def mount(A):
		if A.parent:A.us_states=A.parent.us_states;A.countries=A.parent.countries
		A.fields=[A.name for A in Webscrape._meta.get_fields()];A.table_fields=copy.copy(A.fields)
		for B in A.excluded_fields:
			if B in A.table_fields:A.table_fields.remove(B)
		A.load_table()
	_sort:str=_A
	def get_sort(A,field=_A):
		B=field
		if B:
			C=-1
			if A._sort:
				if B==A._sort[1:]:C=int(A._sort[:1])*-1
			D='-'if C==-1 else'+';A._sort=f"{D}{B}"
		elif not A._sort:A._sort=A.default_sort
		return A._sort
	def sort(C,query_string):
		'\n            Sorts the corresponding table, using querystring to identify which.\n\n            query_string\n                A url parameters like query string variables,\n                Workaround to bypass Unicorn multiple arguments js call issue...\n                @ToDo :: Fix in Unicorn framework (branch?)\n\n                From javascript:\n                    ```js\n                        //* Convert object to query string\n                        const params = { _response, think };\n                        const queryString = new URLSearchParams(params).toString();\n                    ```\n        ';B=query_string;A=_A
		if B:A={A:B[0]for(A,B)in parse_qs(B).items()}
		C.load_table(status=A['status'],sort_field=A['field'])
	def load_table(A,force_render=False,status=_A,sort_field=_A):
		'\n            Description\n                ...\n                Sort happens entirely backend view side, \n                the frontend only sends the field\n\n            Args\n                force_render: bool\n                table: str\n                sort: str\n        ';E='%Y%m%d%H%M%s';F=sort_field;B=status;G=A.get_sort(field=F)
		if not(B and F):
			A.webscrapes=Webscrape.objects.filter(Q(created_on__gt=datetime.datetime(2025,2,11)))
			for C in A.webscrapes:
				if not C.task_attempts:C.task_attempts=0;C.save()
				if A.parent:A.parent.set_queuable_task_queued(webscrape=C)
			A.tables=list(map(lambda status:(status,A.webscrapes.filter(Q(task_status=status)).order_by(G)[:20],A.webscrapes.filter(Q(task_status=status)).order_by('-task_thread_started_at').first()),A.statuses));D=copy.copy(A.tables);D=list(map(lambda x:(x[0],x[1],x[2].task_thread_started_at.strftime(E)if x[2]and x[2].task_thread_started_at else datetime.datetime(1900,1,1).strftime(E)),A.tables));D.sort(key=lambda x:x[2],reverse=True);H=D[0][0],D[0][2]
			if H[1]:A.default_webscrape_status=H[0]
			else:
				for I in A.tables:
					B=I[0];J=I[1]
					if len(J):A.default_webscrape_status=B;break
		else:K=A.statuses.index(B);A.tables[K]=B,A.webscrapes.filter(Q(task_status=B)).order_by(G)[:20]
		A.force_render=force_render
	def reload(A):return redirect('webscrape')
	def force_task_run(A,webscrape=_A):'\n            Description\n            Args\n            Raises\n            Returns\n                ____________________\n                See parent...\n        ';return A.parent.force_task_run(webscrape)
	def messages_display(A,status=_A,message=''):
		B=message;C=status
		if C==MessageStatus.SUCCESS:messages.success(A.request,B)
		elif C==MessageStatus.ERROR:messages.error(A.request,B)