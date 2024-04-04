from django_unicorn.components import UnicornView, QuerySetType
from dashboard.models import Book



class TableView(UnicornView):
    books = Book.objects.none()

    def mount(self):
        print("\n\n------------------- table.__dict__: %s -------------------\n\n" % self.__dict__)
        self.load_table()

    def load_table(self):
        self.books = Book.objects.all()[0:10]

        for child in self.children:
            if hasattr(child, "is_editing"):
                child.is_editing = False


    def set_books(self, books: list):
        print("\n\n------------------- table.books:%s -------------------\n\n" % str(books))
        self.books = books
        self.load_table()
        self.force_reload = True


    def edit(self, pk:int):
        print("\n\n------------------- table.edit - pk:%i -------------------\n\n" % pk)
        child_view = list(filter(lambda x: hasattr(x, "book") and x.book.pk == pk, self.children)) 
        child_view[0].is_editing = True
