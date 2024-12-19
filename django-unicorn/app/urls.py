from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .components.books.books_view import BooksView


urlpatterns = [
    path("", views.index, name='app_index'),
    path("index/", views.index, name='app_index'),
    path("start/", views.start, name='app_start'),

    path("hello_world/", views.hello_world, name='hello_world'),
    path("books_demo/", views.books_demo, name='books_demo'),

    path("books_view/", BooksView.as_view(), name='books_view'),
]
