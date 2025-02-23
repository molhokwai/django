from django_unicorn.components import UnicornView
from webscraping.models import Webscrape
from django_app.settings import _print
class FilterView(UnicornView):
	search=''
	def updated_search(A,query):
		B=query;A.parent.load_table()
		def C(entity,excluded_fields=[]):
			D=entity;A.fields=[A for A in D._meta.get_fields()]
			for B in A.fields:
				if B.name in excluded_fields:A.fields.remove(B)
			C=''
			for B in A.fields:C=f"{C} {str(D.__dict__[B.name])}"
			_print(C,VERBOSITY=3);return C
		if B:A.parent.webscrapes=list(filter(lambda e:B.lower()in C(e,excluded_fields=['id']).lower(),A.parent.webscrapes))
		A.parent.force_render=True