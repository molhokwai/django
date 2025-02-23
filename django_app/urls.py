"\nURL configuration for django_app project.\n\nThe `urlpatterns` list routes URLs to views. For more information please see:\n    https://docs.djangoproject.com/en/4.2/topics/http/urls/\nExamples:\nFunction views\n    1. Add an import:  from my_app import views\n    2. Add a URL to urlpatterns:  path('', views.home, name='home')\nClass-based views\n    1. Add an import:  from other_app.views import Home\n    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')\nIncluding another URLconf\n    1. Import the include() function: from django.urls import include, path\n    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))\n"
_A='site.webmanifest'
from django.contrib import admin
from django.conf import settings
from django.urls import path,include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
urlpatterns=[path('admin/',admin.site.urls),path('unicorn/',include('django_unicorn.urls')),path('',include('app.urls')),path('webscraping/',include('webscraping.urls')),path('__reload__/',include('django_browser_reload.urls')),path('favicon.ico',RedirectView.as_view(url=settings.STATIC_URL+'images/favicon.ico',permanent=True)),path(_A,RedirectView.as_view(url=settings.STATIC_URL+_A,permanent=True))]+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+debug_toolbar_urls()