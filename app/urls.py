from django.urls import path,re_path,include
from django.conf import settings
from django.conf.urls.static import static
from.import views
urlpatterns=[path('',views.journal,name='home'),path('index/',views.journal,name='index'),path('journal/',views.journal,name='journal'),path('webscrape_index/',views.index,name='webscrape_index'),path('login/',views.login_view,name='login'),path('register/',views.register_view,name='register'),path('logout/',views.logout_view,name='logout'),path('error/',views.error,name='error'),path('test_ollama_raw/',views.test_ollama_raw,name='test_ollama_raw')]