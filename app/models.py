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

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    date_published  = models.DateField(null=True, auto_now_add=False)
    country = models.CharField(null=True, max_length=2,  choices=Countries.choices)



class TaskStatus(models.TextChoices):
    """
        TODO = '↗'
        IN_PROGRESS = '~'
        IN_VALIDATION = '⌛'
        ON_HOLD = '|'
        COMPLETED = '✓'
        STOPPED = '✗'
        WHEN_FREE = '☴'
    """
    TODO = '↗', 'TODO'
    IN_PROGRESS = '~', 'IN_PROGRESS'
    IN_VALIDATION = '⌛', 'IN_VALIDATION'
    ON_HOLD = '|', 'ON_HOLD'
    COMPLETED = '✓', 'COMPLETED'
    STOPPED = '✗', 'STOPPED'
    WHEN_FREE = '☴', 'WHEN_FREE'    

    @staticmethod
    def name_value_map():
        return dict(zip(TaskStatus.names, TaskStatus.values))
    def value_name_map():
        return dict(zip(TaskStatus.values, TaskStatus.names))


class TrainingCourse(models.Model):
    """
    Description
        PROMPT
        _______
        Hello Gemini,
        Please generate two models from this structure:

            "course": {
                "key": 2,
                "title": "TRAINING A PROJECT MANAGER",
                "status_text": "Dossier: <a href='https://drive.google.com/drive/u/1/folders/187MK2EMs1QjRtLgDvHnAbTFe6qU4VXBU' target='_blank'>en ligne</a>",
                "sessions": [
                    {
                      "title": "Introduction",
                      "status_text": "Prérequis: Créer votre email - In text format, medias to do...",
                      "preparation": TaskStatus.IN_PROGRESS,
                      "course_media_raw": TaskStatus.TODO,
                      "course_media_final": TaskStatus.TODO,
                      "course_media_validated": TaskStatus.TODO,
                      "implemented_in_app": TaskStatus.TODO,
                      "ready_for_whats_and_gram": TaskStatus.TODO,
                      "in_sales_funnel": TaskStatus.TODO,
                     }
                ]
            }



        - A "Training Course" model
        - A "Training Course Session" model with a "Training Course" Foreign key

        @Todo ?
            - A "Traning Session" model with a "Training Course" ManyToMany relationship, as a training session can belong to many courses
    """
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    status_text = models.TextField()

    date_published = models.DateTimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) 

        # Check for slug conflicts
        while TrainingCourse.objects.filter(slug=self.slug).exists():
            # Add a UUID to the slug to make it unique
            self.slug = f"{slugify(self.title)}-{uuid.uuid4().hex[:8]}"

        super(TrainingCourse, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class TrainingCourseSession(models.Model):
    """
    Description
        See <TrainingCourse>...
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    status_text = models.TextField()
    preparation = models.CharField(max_length=50, choices=TaskStatus.choices)
    course_media_raw = models.CharField(max_length=50, choices=TaskStatus.choices)
    course_media_final = models.CharField(max_length=50, choices=TaskStatus.choices)
    course_media_validated = models.CharField(max_length=50, choices=TaskStatus.choices)
    implemented_in_app = models.CharField(max_length=50, choices=TaskStatus.choices)
    ready_for_whats_and_gram = models.CharField(max_length=50, choices=TaskStatus.choices)
    in_sales_funnel = models.CharField(max_length=50, choices=TaskStatus.choices)
    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE)

    date_published = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) 

        # Check for slug conflicts
        while TrainingCourseSession.objects.filter(slug=self.slug).exists():
            # Add a UUID to the slug to make it unique
            self.slug = f"{slugify(self.title)}-{uuid.uuid4().hex[:8]}"

        super(TrainingCourseSession, self).save(*args, **kwargs)


    def set_choices_display(self, choiceClass=TaskStatus):
        choice_fields = (
            'preparation', 'course_media_raw', 'course_media_final', 'course_media_validated'
            'implemented_in_app', 'ready_for_whats_and_gram', 'in_sales_funnel',
        )
        for field in TrainingCourseSession._meta.get_fields():
            # @ToDo: Adjust code to instead use generic `if fieldname in hasattr(field, "choices")` ?
            if field.name in choice_fields:
                for value in choiceClass.values:
                    name = choiceClass.value_name_map()[value]
                    if value == getattr(self, str(field.name)):
                        field_name_attr = f"{field.name}_name"
                        field_label_attr = f"{field.name}_label"

                        self.__dict__[field_name_attr] = name
                        self.__dict__[field_label_attr] = value
                        # check:
                        # -----
                        # print(field.name, field_label_attr, self.__dict__[field_label_attr])


    def __str__(self):
        return self.title


    class Meta:
        unique_together = (('title', 'course'),)


