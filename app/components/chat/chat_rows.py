from django.core.paginator import Paginator
from django_unicorn.components import UnicornView
from app.models import ChatPromptAndResponse
import math,markdown
class ChatRowsView(UnicornView):
	'\n    Displays the last 10 chat rows with pagination for older rows.\n    ';chats=[];page_number=1;nr_of_pages=None;items_per_page=3
	def mount(A):A.load_chats()
	def load_chats(B,force_render=False):
		C=ChatPromptAndResponse.objects.all()
		if False:
			for A in C:A.prompt=markdown.markdown(A.prompt);A.response=markdown.markdown(A.response);A.think=markdown.markdown(A.think);A.save()
		D=Paginator(C,B.items_per_page);B.nr_of_pages=int(math.ceil(len(C)/B.items_per_page));B.chats=D.page(B.page_number).object_list;B.force_render=force_render
	def next_page(A):A.page_number+=1;A.load_chats()
	def previous_page(A):
		if A.page_number>1:A.page_number-=1;A.load_chats()