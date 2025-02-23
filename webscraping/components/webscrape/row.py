from django_unicorn.components import UnicornView

from django_app.settings import _print, WEBSCRAPER_TASK_MAX_ATTEMPTS
from .webscrape import MessageStatus
from webscraping.models import Webscrape
from webscraping.modules.threader.classes.TaskHandler import TaskHandler



class RowView(UnicornView):
    webscrape = None
    is_editing = False

    countries = None
    us_states = None

    excluded_fields = None

    task_output = ''

    task_is_queueable = False

    task_maxed_attempts = False


    def mount(self):
        self.us_states = self.parent.us_states
        self.countries = self.parent.countries

        self.excluded_fields = self.parent.excluded_fields

        _print('webscrape.RowView.mount → type(self.webscrape) == type(dict): %s' \
              % str(type(self.webscrape) == type({})), 
              VERBOSITY=3
        )

        self.load()


    def load(self, force_render=False):
        if type(self.webscrape) == type({}):
            # sep: "-------ktou##################outk-------" ?
            # ---------------------------
            _print(
                'webscrape.RowView.mount → task_run_id : %s ' % str(self.webscrape["task_run_id"]),
                VERBOSITY=3
            )

            self.webscrape = Webscrape.objects.get(task_run_id=self.webscrape["task_run_id"])
        else:
            _print(
                'webscrape.RowView.mount → task_run_id : %s' % self.webscrape.task_run_id,
                VERBOSITY=3
            )

        if self.webscrape.task_output:
            self.task_output = self.webscrape.task_output.replace('\\t', '  ').replace('\\n', '<br/>')

        self.task_is_queueable = TaskHandler.task_is_queueable(self.webscrape)

        self.task_maxed_attempts = self.webscrape.task_attempts >= WEBSCRAPER_TASK_MAX_ATTEMPTS

        self.force_render = force_render


    def edit(self):
        self.is_editing = True


    def cancel(self):
        self.is_editing = False


    def retry(self, webscrape_id: str):

        webscrape = Webscrape.objects.get(id=int(webscrape_id))
        _print(f'webscrape.RowView.retrying → webscrape.id: {webscrape.id}...', 
              VERBOSITY=0
        )

        if self.parent:
            _print(f'webscrape.RowView.retry → {webscrape.firstName} {webscrape.lastName} '
                   f' | {type(webscrape)}', 
                  VERBOSITY=0
            )
            self.parent.force_task_run(webscrape)
            self.call("highlight_row", f"retry-{webscrape.id}")
        else:
            _print(f'webscrape.RowView.retry → NO PARENT', 
                  VERBOSITY=0
            )
            self.call("highlight_row_error", f"retry-{webscrape.id}")


    def save(self):
        """
        Description
            @debug
                _print( '........', VERBOSITY=3 )
        """
        self.webscrape.save()

        self.is_editing = False
        self.parent.messages_display(MessageStatus.SUCCESS, "Item saved.")
        self.parent.load_table()

