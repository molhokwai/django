from django_unicorn.components import UnicornView

from .table import MessageStatus



class RowView(UnicornView):
    book = None
    is_editing = False

    countries = None


    def mount(self):
        self.countries = self.parent.countries


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
        self.book.save()
        self.is_editing = False
        self.parent.messages_display(MessageStatus.SUCCESS, "Item saved.")
        self.parent.load_table(force_render=True)

