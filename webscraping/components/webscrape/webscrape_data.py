from django_unicorn.components import UnicornView
from django.shortcuts import redirect
from django.contrib import messages
from webscraping.views import parse_raw_outputs
from enum import Enum
class MessageStatus(Enum):SUCCESS='Success';ERROR='Error';NOTICE='Notice'
class WebscrapeDataView(UnicornView):
	aggregated_results=[];aggregated_results_table_fields=['NAME','AGE','LOCATION','POSSIBLE_RELATIVES','VERIFIED','CRIMINAL_RECORDS']
	def mount(A):A.aggregated_results=parse_raw_outputs();A.load_table()
	def load_table(A,force_render=False):A.force_render=force_render
	def reload(A):return redirect('webscrape_data')
	def messages_display(A,status=None,message=''):
		B=message;C=status
		if C==MessageStatus.SUCCESS:messages.success(A.request,B)
		elif C==MessageStatus.ERROR:messages.error(A.request,B)