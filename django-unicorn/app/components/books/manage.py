from django_unicorn.components import UnicornView, QuerySetType
from datetime import date
from app.models import Book

from .table import MessageStatus


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

    books: QuerySetType[Book] = Book.objects.all()


    def mount(self):
        self.countries = self.parent.countries


    def save_file(self):
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
        self.save_file()

        print('------------------ %s, %s, %s ----------------' % (self.title, self.author, self.country))
        Book.objects.create(
            title = self.title,
            author = self.author,
            date_published = self.date_published,
            country = self.country,
        )
        self.clear_fields()
        return self.parent.reload()

    def delete(self):
        Book.objects.filter(title=self.title).delete()
        self.parent.messages_display(MessageStatus.SUCCESS, "Item deleted.")
        return self.parent.reload()


    def delete_all(self):
        Book.objects.all().delete()
        self.parent.messages_display(MessageStatus.SUCCESS, "All items deleted.")
        self.update_list()


    def update_list(self):
        self.parent.load_table(force_render=True)


    def clear_fields(self):
        self.title = ''
        self.author = ''
        self.date_published = ''
