from django_unicorn.components import UnicornView


class FilterView(UnicornView):
    search = ""

    def updated_search(self, query):
        self.parent.load_table()

        if query:
            self.parent.books = list(
                 filter(lambda f: query.lower() in f.title.lower(), self.parent.books)
            )

        self.parent.force_render = True


    # @cached_property
    # def countries(self):
    #     return 
