_A=False
from django_unicorn.components import UnicornView
from django_app.settings import _print
from.webscrapes import MessageStatus
class RowView(UnicornView):
	webscrape=None;is_editing=_A;countries=None;us_states=None
	def mount(A):A.us_states=A.parent.us_states;A.countries=A.parent.countries
	def edit(A):A.is_editing=True
	def cancel(A):A.is_editing=_A
	def save(A):"\n        Description\n            @debug\n                _print('...........', VERBOSITY=3)\n        ";A.webscrape.save();A.is_editing=_A;A.parent.messages_display(MessageStatus.SUCCESS,'Item saved.');A.parent.load_table(force_render=True);return A.parent.reload()