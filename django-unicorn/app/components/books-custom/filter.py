from django_unicorn.components import UnicornView, QuerySetType

class FilterView(UnicornView):
    search = ""

    def updated_search(self, query):
        if query:
            self.parent.set_books(list(
                filter(lambda f: query.lower() in f.title.lower(), self.parent.books)
            ))

        print("\n\n------------------- children: %s -------------------\n\n" % str(self.parent.children))
        for child in self.parent.children:
            print("\n\n------------------- child.__dict__: %s -------------------\n\n" % child.__dict__)
