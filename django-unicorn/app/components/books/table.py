from django_unicorn.components import LocationUpdate, UnicornView, QuerySetType
from django.shortcuts import redirect
from django.contrib import messages
from app.models import Book

from enum import Enum
import copy

class MessageStatus(Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    NOTICE = "Notice"


class TableView(UnicornView):
    books = Book.objects.none()
    countries = None
    fields = None
    table_fields = None


    def mount(self):
        self.countries = list(zip(Book.Countries.values, Book.Countries.names))
        self.fields = [f.name for f in Book._meta.get_fields()]
        self.table_fields = copy.copy(self.fields)
        self.table_fields.remove('id')
        self.load_table()


    def load_table(self, force_render=False):
        self.books = Book.objects.all().order_by("author")
        if len(self.books):
            self.books = self.books[0:10]
        self.force_render = force_render


    def reload(self):
        return redirect('books_demo')


    def messages_display(self, status:MessageStatus=None, message:str=""):
        if status == MessageStatus.SUCCESS:
            messages.success(self.request, message)
        elif status  == MessageStatus.ERROR:
            messages.error(self.request, message)


    def add_count(self):
        messages.success(self.request, "| %i books loaded..." % len(self.books))
