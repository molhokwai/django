from django_unicorn.components import UnicornView
from django_unicorn.components import UnicornView, QuerySetType
from django.db.models.query_utils import Q

from datetime import date
from darklight.models import Blog, BlogPost


from enum import Enum

class MessageStatus(Enum):
    SUCCESS = "Success"
    ERROR = "Error"
    NOTICE = "Notice"



class BlogView(UnicornView):
    """
        src: https://www.bugbytes.io/posts/django-unicorn-an-introduction/
    """

    blog_title: str = None
    blog: Blog = None
    blogposts: QuerySetType[BlogPost] = None

    # def __init__(self, *args, **kwargs):
    #     self.blog_title = kwargs["blog_title"]

    def mount(self):
        try:

            self.blog = Blog.objects.get(title=self.blog_title)
            key_filter = Q(blog__title=self.blog_title)
            self.blogposts = BlogPost.objects.filter(key_filter)

        except Blog.DoesNotExist as err:
            self.messages_display(MessageStatus.NOTICE, "No blog with title '%s' created yet." % self.blog_title)


    def messages_display(self, status:MessageStatus=None, message:str=""):
        if status == MessageStatus.SUCCESS:
            messages.success(self.request, message)
        elif status  == MessageStatus.ERROR:
            messages.error(self.request, message)
