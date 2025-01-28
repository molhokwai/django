from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .components.blogpost import BlogpostView


urlpatterns = [
    path("", views.index, name='darklight_index'),
    path("post/<str:title>", BlogpostView.as_view(), name='blogpost_view'),
]
