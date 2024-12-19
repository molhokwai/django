from django_unicorn.components import UnicornView
from darklight.models import BlogPost, Image

class BlogpostView(UnicornView):
    blogpost_view = 'blogpost_view'
    blogpost: BlogPost = None
    images: list = None


    def mount(self):
        if "blogpost" in self.kwargs:
            self.blogpost = self.kwargs["blogpost"]
        elif "title" in self.kwargs:
            self.blogpost = BlogPost.objects.get(title=self.kwargs["title"])

        if self.blogpost:
            self.images = []
            for image in self.blogpost.images.all():
                self.images.append(image)
