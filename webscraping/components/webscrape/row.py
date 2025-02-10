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
        if type(self.webscrape) == type({}):
            # sep: "-------ktou##################outk-------" ?
            # ---------------------------
            _print(
                'webscrape.RowView.mount → task_id : %s ' % str(self.webscrape["task_id"]),
                VERBOSITY=3
            )

            self.webscrape = Webscrape.objects.get(task_id=self.webscrape["task_id"])
        else:
            _print(
                'webscrape.RowView.mount → task_id : %s' % self.webscrape.task_id,
                VERBOSITY=3
            )

        if self.webscrape.task_output:
            self.task_output = self.webscrape.task_output.replace('\\t', '  ').replace('\\n', '<br/>')


    def edit(self):
        self.is_editing = True


    def cancel(self):
        self.is_editing = False


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

        return self.parent.reload()

