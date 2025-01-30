from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User


from tinymce.models import HTMLField
from taggit.managers import TaggableManager
# from taggit.serializers import TagListSerializerField, TaggitSerializer



defaults = {
    "img" : "/static/templates/main/img/cover_images/post/choose-and-image-fr.png",
    "post" : {
        "cover_image": "/static/templates/main/img/cover_images/post/choose-and-image-fr.png"
    }
    
}

class Image(models.Model):
    """
        ...
    """
    admin = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name="image_admin", editable=True)    # , default=get_current_user
    title = models.CharField(max_length=200, unique=True, null=True, blank=True, default=_('Le nom/titre de l’image ici...'))
    description = HTMLField(null=True, blank=True, default='La description ici...')
    image_file = models.ImageField(default=defaults['img'], upload_to='img/unsorted')    
    tags = TaggableManager()
    date_uploaded  = models.DateTimeField(auto_now_add=False, default=timezone.now)


    def get_absolute_url(self):
        return reverse("img", args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["date_uploaded"]



class Category(models.Model):
    """
    @description
        slug
            source: https://www.geeksforgeeks.org/add-the-slug-field-inside-django-model/
            See #Modify URL with Slug for category pages url...

        Usage:
            ```
            ```
    @todo :: DELETE AFTER SUCCESSFULL TEST
        __

        Hello Gemini,

        With the model below, how to automatically save sanitized category name from title, that is: Replacing spaces with "_" or "-" , all in lowercase, unicode to ascii characters, and only alphanumeric...?

    countries :: https://stackoverflow.com/questions/2963930/django-country-drop-down-list/62471903#62471903

        ```
        class Category(models.Model):

          title = models.CharField(max_length=200, unique=True, null=False, blank=False, default='Le titre ici...')
          name = models.CharField(max_length=200, unique=True, null=False, blank=False, default='Le nom ici...')
          description = HTMLField(null=False, blank=False, default='La description ici...')

          history = HistoricalRecords()

        ```
    """
    title = models.CharField(max_length=200, unique=True, null=False, blank=False, default=_('Le nom/titre de la catégorie ici...'))
    slug = models.SlugField(max_length = 250, null=True, blank=True)
    description = HTMLField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=False, default=timezone.now)


    def get_absolute_url(self):
        return reverse("cat", args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]



class Blog(models.Model):
    """
        ...
    """
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_admin", editable=True)
    title = models.CharField(max_length=200, unique=True, null=False, blank=False, default=_('Le titre du blog ici...'))    
    slug = models.SlugField(max_length = 250, null=True, blank=True)
    description = HTMLField(null=False, blank=False, default='Le contenu ici...')

    editors = models.ManyToManyField(User, blank=True, related_name="blog_editors")

    date_created  = models.DateTimeField(auto_now_add=False, default=timezone.now)


    def get_absolute_url(self):
        return reverse("blog", args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["date_created"]



class BlogPost(models.Model):
    """
        @ToDo :: set images:  upload_to='img/cover_images/blogpost'
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blogpost_blog", editable=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogpost_admin", editable=True)

    title = models.CharField(max_length=200, unique=True, null=False, blank=False, default=_('Le titre du post ici...'))    
    slug = models.SlugField(max_length = 250, null=True, blank=True)
    description = HTMLField(null=False, blank=False, default='Le contenu ici...')
    images = models.ManyToManyField(Image, related_name='blogpost_image')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                            related_name="post_category", null=True, blank=True)
    tags = TaggableManager()
    editors = models.ManyToManyField(User, related_name="blogpost_editors")

    date_created = models.DateTimeField(auto_now_add=False, default=timezone.now)


    def get_absolute_url(self):
        return reverse("post", args=[self.id])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["date_created"]


