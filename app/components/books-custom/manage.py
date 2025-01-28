from django_unicorn.components import UnicornView, QuerySetType
from dashboard.models import Book
from datetime import date


class ManageView(UnicornView):
    """
        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/
    """
    title: str = ''
    author: str = ''
    date_published: date = None
    books: QuerySetType[Book] = Book.objects.all()


    def mount(self):
        args = self.component_args
        kwargs = self.component_kwargs

        self.update_list()


    def add(self):
        print('------------------ %s, %s ----------------' % (self.title, self.author))
        Book.objects.create(
            title = self.title,
            author = self.author,
            date_published = self.date_published,
        )
        self.update_list()
        self.clear_fields()


    def delete(self):
        print('------------------ %s ----------------' % self.title)
        Book.objects.filter(title=self.title).delete()
        self.update_list()


    def delete_all(self):
        Book.objects.all().delete()
        self.update_list()


    def update_list(self):
        self.books = Book.objects.all()


    def clear_fields(self):
        self.title = ''
        self.author = ''
