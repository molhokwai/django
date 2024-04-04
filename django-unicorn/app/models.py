from django.db import models
from django.utils.translation import gettext_lazy as _


class Book(models.Model):

    class Countries(models.TextChoices):
        CAMEROUN = 'CM', _('Cameroon')
        CANADA = 'CA', _('Canada')
        FRANCE = 'FR', _('France')
        NIGERIA = 'NG', _('Nigeria')
        USA = 'US', _('USA')
        UK = 'UK', _('United Kingdom')


    title = models.CharField(max_length=200)    
    author = models.CharField(max_length=200)
    date_published  = models.DateField(null=True, auto_now_add=False)
    country = models.CharField(null=True, max_length=2,  choices=Countries.choices)
