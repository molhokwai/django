_B=None
_A=False
from django_unicorn.components import UnicornView
from django_app.settings import _print,WEBSCRAPER_TASK_MAX_ATTEMPTS
from.webscrape import MessageStatus
from webscraping.models import Webscrape
from webscraping.modules.threader.classes.TaskHandler import TaskHandler
class RowView(UnicornView):
	webscrape=_B;is_editing=_A;countries=_B;us_states=_B;excluded_fields=_B;task_output='';task_is_queueable=_A;task_maxed_attempts=_A
	def mount(A):A.us_states=A.parent.us_states;A.countries=A.parent.countries;A.excluded_fields=A.parent.excluded_fields;_print('webscrape.RowView.mount → type(self.webscrape) == type(dict): %s'%str(type(A.webscrape)==type({})),VERBOSITY=3);A.load()
	def load(A,force_render=_A):
		B='task_run_id'
		if type(A.webscrape)==type({}):_print('webscrape.RowView.mount → task_run_id : %s '%str(A.webscrape[B]),VERBOSITY=3);A.webscrape=Webscrape.objects.get(task_run_id=A.webscrape[B])
		else:_print('webscrape.RowView.mount → task_run_id : %s'%A.webscrape.task_run_id,VERBOSITY=3)
		if A.webscrape.task_output:A.task_output=A.webscrape.task_output.replace('\\t','  ').replace('\\n','<br/>')
		A.task_is_queueable=TaskHandler.task_is_queueable(A.webscrape);A.task_maxed_attempts=A.webscrape.task_attempts>=WEBSCRAPER_TASK_MAX_ATTEMPTS;A.force_render=force_render
	def edit(A):A.is_editing=True
	def cancel(A):A.is_editing=_A
	def retry(B,webscrape_id):
		A=Webscrape.objects.get(id=int(webscrape_id));_print(f"webscrape.RowView.retrying → webscrape.id: {A.id}...",VERBOSITY=0)
		if B.parent:_print(f"webscrape.RowView.retry → {A.firstName} {A.lastName}  | {type(A)}",VERBOSITY=0);B.parent.force_task_run(A);B.call('highlight_row',f"retry-{A.id}")
		else:_print(f"webscrape.RowView.retry → NO PARENT",VERBOSITY=0);B.call('highlight_row_error',f"retry-{A.id}")
	def save(A):"\n        Description\n            @debug\n                _print( '........', VERBOSITY=3 )\n        ";A.webscrape.save();A.is_editing=_A;A.parent.messages_display(MessageStatus.SUCCESS,'Item saved.');A.parent.load_table()