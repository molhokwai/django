from django_unicorn.components import UnicornView, QuerySetType
from django.conf import settings

from django_app.settings import _print
from webscraping.models import Webscrape
from .webscrapes import MessageStatus

from datetime import date, datetime

class ManageView(UnicornView):
    """
        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/
    """
    webscrape: Webscrape = None


    website_url: str = ''
    title: str = ''
    first_name: str = ''
    last_name: str = ''
    middle_name: str = ''
    middle_initials: str = ''
    age: int = None
    city: str = ''
    state: str = ''
    country: str = '' 

    us_states = None
    countries = None

    new_media_base64 = None
    new_media_file_name = None

    webscrapes: QuerySetType[Webscrape] = Webscrape.objects.all()

    def setTitle(self, value):
        self.title = value

    def mount(self):
        self.countries = self.parent.countries
        self.us_states = self.parent.us_states

        # For testing...
        # --------------
        if settings.DEBUG:
            self.webscrape = Webscrape.objects.first()

        # Instance fields and values: get
        # ----------------------
        # from django.forms.models import model_to_dict
        # print(model_to_dict(self.webscrape))

        # @ToDo: Auto set fields - check
        # ----------------------
        # self.fields = [f.name for f in Webscrape._meta.get_fields()]
        # for val in ('id', 'created_on', 'last_modified'):
        #     self.fields.remove(val)

        # for field in self.fields:
        #     self.__dict__[field] = None


    def save_file(self):
        """
        DJANGO UNICORN FILE UPLOADS - From https://github.com/adamghill/django-unicorn/discussions/256

        Test Data:
            Emke – The Threepenny Review
            Imbolo Mbue
            2015-05-13
            /home/nkensa/GDrive-local/Tree/Webscrapes/Imbolo_Mbue_Emke_The_Threepenny_Review.pdf
        """

        image_data = self.new_media_base64.split(';base64,')[-1]  # Extract the base64 image data
        decoded_image = b64decode(image_data)
        if len(decoded_image) > 10 * 1024 * 1024:  # 10MB limit
            raise "File exceeds the 10mb limit."

        self.new_media_err = None
        media = Media(
            name=self.new_media_file_name,
        )
        media.src.save(self.generate_unique_media_name(), ContentFile(decoded_image), save=True)


    def add(self):
        # ?
        # -
        # self.save_file()

        _print(
            '------------------ | ---------------- %s, %s' % str(self.title), str(self.age), 
            VERBOSITY=3
        )
        Webscrape.objects.create(
            website_url = self.website_url,
            title = self.title,
            first_name = self.first_name,
            last_name = self.last_name,
            middle_name = self.middle_name,
            middle_initials = self.middle_initials,
            age = self.age,
            city = self.city,
            state = self.state,
        )
        self.clear_fields()
        return self.parent.reload()

    def delete(self):
        Webscrape.objects.filter(title=self.title).delete()
        self.parent.messages_display(MessageStatus.SUCCESS, "Item deleted.")
        return self.parent.reload()


    def delete_all(self):
        Webscrape.objects.all().delete()
        self.parent.messages_display(MessageStatus.SUCCESS, "All items deleted.")
        self.update_list()


    def update_list(self):
        self.parent.load_table(force_render=True)


    def unique_title(self):
        if self.title:
            self.title = f"{self.title} | {datetime.now()}"

        elif self.last_name:
            self.title = f"{self.last_name} | {datetime.now()}" 
            if self.first_name:
                self.title = f"{self.first_name} {self.title}" 


    def clear_fields(self):
        self.title = ''
        self.first_name = ''
        self.last_name = ''
        self.middle_name = ''
        self.middle_initials = ''
        self.last_name = ''
        self.age = ''
        self.city = ''
        self.state = ''


