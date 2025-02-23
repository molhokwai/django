_A=None
from django_unicorn.components import UnicornView,QuerySetType
from django.conf import settings
from django_app.settings import _print
from webscraping.models import Webscrape
from.webscrapes import MessageStatus
from datetime import date,datetime
class ManageView(UnicornView):
	'\n        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/\n    ';webscrape:Webscrape=_A;website_url:str='';title:str='';first_name:str='';last_name:str='';middle_name:str='';middle_initials:str='';age:int=_A;city:str='';state:str='';country:str='';us_states=_A;countries=_A;new_media_base64=_A;new_media_file_name=_A;webscrapes:QuerySetType[Webscrape]=Webscrape.objects.all()
	def setTitle(A,value):A.title=value
	def mount(A):
		A.countries=A.parent.countries;A.us_states=A.parent.us_states
		if settings.DEBUG:A.webscrape=Webscrape.objects.first()
	def save_file(A):
		'\n        DJANGO UNICORN FILE UPLOADS - From https://github.com/adamghill/django-unicorn/discussions/256\n\n        Test Data:\n            Emke – The Threepenny Review\n            Imbolo Mbue\n            2015-05-13\n            /home/nkensa/GDrive-local/Tree/Webscrapes/Imbolo_Mbue_Emke_The_Threepenny_Review.pdf\n        ';C=A.new_media_base64.split(';base64,')[-1];B=b64decode(C)
		if len(B)>10485760:raise'File exceeds the 10mb limit.'
		A.new_media_err=_A;D=Media(name=A.new_media_file_name);D.src.save(A.generate_unique_media_name(),ContentFile(B),save=True)
	def add(A):_print('------------------ | ---------------- %s, %s'%str(A.title),str(A.age),VERBOSITY=3);Webscrape.objects.create(website_url=A.website_url,title=A.title,first_name=A.first_name,last_name=A.last_name,middle_name=A.middle_name,middle_initials=A.middle_initials,age=A.age,city=A.city,state=A.state);A.clear_fields();return A.parent.reload()
	def delete(A):Webscrape.objects.filter(title=A.title).delete();A.parent.messages_display(MessageStatus.SUCCESS,'Item deleted.');return A.parent.reload()
	def delete_all(A):Webscrape.objects.all().delete();A.parent.messages_display(MessageStatus.SUCCESS,'All items deleted.');A.update_list()
	def update_list(A):A.parent.load_table(force_render=True)
	def unique_title(A):
		if A.title:A.title=f"{A.title} | {datetime.now()}"
		elif A.last_name:
			A.title=f"{A.last_name} | {datetime.now()}"
			if A.first_name:A.title=f"{A.first_name} {A.title}"
	def clear_fields(A):A.title='';A.first_name='';A.last_name='';A.middle_name='';A.middle_initials='';A.last_name='';A.age='';A.city='';A.state=''