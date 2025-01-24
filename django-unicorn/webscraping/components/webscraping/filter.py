from django_unicorn.components import UnicornView


class FilterView(UnicornView):
    search = ""

    def updated_search(self, query):
        self.parent.load_table()

        if query:
            self.parent.webscrapes = list(
                 filter(lambda f: query.lower() in f.title.lower(), self.parent.webscrapes)
            )

        self.parent.force_render = True


    # @cached_property
    # def countries(self):
    #     return 
