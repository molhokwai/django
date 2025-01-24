from django.db import models
from django.utils.translation import gettext_lazy as _

from django.utils.text import slugify

import uuid


class Countries(models.TextChoices):
    """
        Description
            Usage
                view:
                    ```python
                        self.countries = list(zip(Countries.values, Countries.names))
                    ```
                template:
                    ```html
                        <select id="country">
                            <option>Select a country...</option>
                            {% for country in countries %}
                                <option value="{{ country.0 }}">{{ country.1 }}</option>
                            {% endfor %}
                        </select>
                    ```
    """
    CAMEROUN = 'CM', _('Cameroon')
    CANADA = 'CA', _('Canada')
    FRANCE = 'FR', _('France')
    NIGERIA = 'NG', _('Nigeria')
    USA = 'US', _('USA')
    UK = 'UK', _('United Kingdom')


class USStates(models.TextChoices):
    """
        Description
            Usage
                view:
                    ```python
                        self.states = list(zip(USStates.values, USStates.names))
                    ```
                template:
                    ```html
                        <select id="state">
                            <option>Select a state...</option>
                            {% for state in states %}
                                <option value="{{ state.0 }}">{{ state.1 }}</option>
                            {% endfor %}
                        </select>
                    ```
    """
    CALIFORNIA = 'CA', _('California')
    FLORIDA = 'FL', _('Florida')
    NEW_JERSEY = 'NJ', _('New Jersey')
    WASHINGTON = 'WA', _('Washington')
    WINSCONSIN = 'WI', _('Wisconsin')


class Webscrape(models.Model):
    # website
    # -------
    website_url = models.CharField(max_length=200, default="https://wwww.truthfinder.com/")

    # metas
    # -----
    title = models.CharField(max_length=200, unique=True, null=False, blank=False)

    # identification
    # --------------
    first_name = models.CharField(max_length=200, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    middle_name = models.CharField(max_length=200)
    middle_initials = models.CharField(max_length=6)
    age = models.IntegerField(max_length=3)

    # location
    # --------
    city = models.CharField(null=True, max_length=200)
    state = models.CharField(null=True, max_length=2,  choices=USStates.choices)
    country = models.CharField(null=True, max_length=2,  choices=Countries.choices, default="US")

    # crud datetimes
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

