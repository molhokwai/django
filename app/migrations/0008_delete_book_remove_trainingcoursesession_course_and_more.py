# Generated by Django 5.1.5 on 2025-02-08 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_trainingcoursesession_course_media_final_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Book',
        ),
        # migrations.RemoveField(
        #     model_name='trainingcoursesession',
        #     name='course',
        # ),
        migrations.AlterUniqueTogether(
            name='trainingcoursesession',
            unique_together=None,
        ),
        migrations.DeleteModel(
            name='TrainingCourse',
        ),
        migrations.DeleteModel(
            name='TrainingCourseSession',
        ),
    ]
