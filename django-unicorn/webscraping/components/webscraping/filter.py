from django_unicorn.components import UnicornView
from webscraping.models import Webscrape

class FilterView(UnicornView):
    search = ""

    def updated_search(self, query):
        self.parent.load_table()

        def entity_full_text(entity, excluded_fields=[]):
            self.fields = [f for f in entity._meta.get_fields()]
            for f in self.fields:
                if f.name in excluded_fields:
                    self.fields.remove(f)

            fulltext = ""
            for f in self.fields:                
                fulltext = f"{fulltext} {str(entity.__dict__[f.name])}"
            print(fulltext)
            return fulltext

        if query:
            self.parent.webscrapes = list(
                 filter(lambda e: query.lower() in \
                     entity_full_text(e, excluded_fields=['id']).lower(), 
                                                                     self.parent.webscrapes)
            )

        self.parent.force_render = True


    # @cached_property
    # def countries(self):
    #     return 
