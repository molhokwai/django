from django_unicorn.components import UnicornView


class RowView(UnicornView):
    book = None
    is_editing = False


    def edit(self):
        print("------------------- table.edit -------------------")
        self.is_editing = True


    def cancel(self):
        self.is_editing = False


    def save(self):
        self.book.save()
        self.is_editing = False