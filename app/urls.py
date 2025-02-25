from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    # pages
    path("", views.index, name='home'),
    path("index/", views.index, name='index'),
    path("webscrape_index/", views.index, name='webscrape_index'),
    path("journal/", views.journal, name='journal'),
    # auth
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    # handlers
    path("error/", views.error, name='error'),
    # tests
    path("test_ollama_raw/", views.test_ollama_raw, name='test_ollama_raw'),
]

