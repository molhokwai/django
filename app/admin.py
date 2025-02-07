from django.contrib import admin
from django.db import models

from .models import Book, TrainingCourse, TrainingCourseSession

admin.site.register(Book)
admin.site.register(TrainingCourse)
admin.site.register(TrainingCourseSession)

