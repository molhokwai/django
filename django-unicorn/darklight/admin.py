from django.contrib import admin

from .models import (
    Image, Category, Blog, BlogPost,
)

admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(BlogPost)

