_A=None
from django_unicorn.components import LocationUpdate,UnicornView,QuerySetType
from django.shortcuts import redirect
from django.contrib import messages
from webscraping.models import Webscrape,Countries,USStates
from enum import Enum
import copy
class MessageStatus(Enum):SUCCESS='Success';ERROR='Error';NOTICE='Notice'
class WebscrapesView(UnicornView):
	webscrapes=Webscrape.objects.none();us_states=_A;countries=_A;fields=_A;table_fields=_A
	def mount(A):
		A.us_states=list(zip(USStates.values,USStates.names));A.countries=list(zip(Countries.values,Countries.names));A.fields=[A.name for A in Webscrape._meta.get_fields()];A.table_fields=copy.copy(A.fields)
		for B in A.fields:
			if B not in('website_url','firstName','lastName','age','city','state'):A.table_fields.remove(B)
		A.load_table()
	def load_table(A,force_render=False):A.webscrapes=Webscrape.objects.all().order_by('-created_on');A.force_render=force_render
	def reload(A):return redirect('webscraping')
	def messages_display(A,status=_A,message=''):
		B=message;C=status
		if C==MessageStatus.SUCCESS:messages.success(A.request,B)
		elif C==MessageStatus.ERROR:messages.error(A.request,B)
	def add_count(A):messages.success(A.request,'| %i webscrapes loaded...'%len(A.webscrapes))