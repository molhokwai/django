from django_unicorn.components import UnicornView

from django_app.settings import _print
from .webscrape import MessageStatus
from webscraping.models import Webscrape



class RowView(UnicornView):
    webscrape = None
    is_editing = False

    countries = None
    us_states = None

    excluded_fields = None

    task_output = ''


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

        self.force_render = force_render


    def edit(self):
        self.is_editing = True


    def cancel(self):
        self.is_editing = False


    def retry(self):
        if self.parent:
            _print(f'webscrape.RowView.retry → {self.webscrape.firstName} {self.webscrape.lastName} '
                   f' | {type(self.webscrape)}', 
                  VERBOSITY=0
            )
            self.parent.set_queuable_task_queued(self.webscrape)
            self.load(force_render = True)
            self.call("highlight_row", f"retry-{self.webscrape.id}")
        else:
            _print(f'webscrape.RowView.retry → NO PARENT', 
                  VERBOSITY=0
            )
            self.call("highlight_row_error", f"retry-{self.webscrape.id}")


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

