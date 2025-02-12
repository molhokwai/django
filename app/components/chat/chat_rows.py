from django.core.paginator import Paginator
from django_unicorn.components import UnicornView
from app.models import ChatPromptAndResponse

import math

class ChatRowsView(UnicornView):
    """
    Displays the last 10 chat rows with pagination for older rows.
    """
    chats = []
    page_number = 1
    nr_of_pages = None
    items_per_page = 3

    def mount(self):
        self.load_chats()

    def load_chats(self, force_render=False):
        # Load the last 10 chats
        rows = ChatPromptAndResponse.objects.all()
        paginator = Paginator(rows, self.items_per_page)

        self.nr_of_pages = int(math.ceil(len(rows) / self.items_per_page))
        self.chats = paginator.page(self.page_number).object_list

        self.force_render = force_render

    def next_page(self):
        # Load the next page of chats
        self.page_number += 1
        self.load_chats()

    def previous_page(self):
        # Load the previous page of chats
        if self.page_number > 1:
            self.page_number -= 1
            self.load_chats()


