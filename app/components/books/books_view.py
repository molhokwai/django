from django_unicorn.components import UnicornView
from app.models import Book


class BooksView(UnicornView):
    template_name = "unicorn/books/books-view.html"

    books = Book.objects.none()

    def mount(self):
        self.books = Book.objects.all().order_by("author")
