from django_unicorn.components import UnicornView, QuerySetType
from datetime import date
from app.models import Webscrape

from .webscrapes import MessageStatus


class ManageView(UnicornView):
    """
        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/
    """
    title: str = ''
    author: str = ''
    date_published: date = None
    country: str = None 

    countries = None

    new_media_base64 = None
    new_media_file_name = None

    webscrapes: QuerySetType[Webscrape] = Webscrape.objects.all()


    def mount(self):
        self.countries = self.parent.countries


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

        print('------------------ %s, %s, %s ----------------' % (self.title, self.author, self.country))
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


