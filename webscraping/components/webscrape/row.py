from django_unicorn.components import UnicornView

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

        if type(self.webscrape) == type({}):
            # sep: "-------ktou##################outk-------" ?
            # ---------------------------
            self.webscrape = Webscrape.objects.get(task_id=self.webscrape["task_id"])
            self.task_output = self.webscrape.task_output


    def edit(self):
        self.is_editing = True


    def cancel(self):
        self.is_editing = False


    def save(self):
        """
        Description
            @debug
                print('\n\n----------------- RowView.book: %i, %s, %s, %s, %s -----------------\n\n' \
                                % (self.book.pk, self.book.title, self.book.author, str(self.book.date_published), self.book.country))
        """
        self.webscrape.save()
        self.is_editing = False
        self.parent.messages_display(MessageStatus.SUCCESS, "Item saved.")
        self.parent.load_table(force_render=True)

        return self.parent.reload()

