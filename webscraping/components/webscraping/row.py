from django_unicorn.components import UnicornView

from django_app.settings import _print
from .webscrapes import MessageStatus



class RowView(UnicornView):
    webscrape = None
    is_editing = False

    countries = None
    us_states = None


    def mount(self):
        self.us_states = self.parent.us_states
        self.countries = self.parent.countries


    def edit(self):
        self.is_editing = True


    def cancel(self):
        self.is_editing = False


    def save(self):
        """
        Description
            @debug
                _print('...........', VERBOSITY=3)
        """
        self.webscrape.save()
        self.is_editing = False
        self.parent.messages_display(MessageStatus.SUCCESS, "Item saved.")
        self.parent.load_table(force_render=True)
        return self.parent.reload()

