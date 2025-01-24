# Generated by Django 5.1.5 on 2025-01-22 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_book_country"),
    ]

    operations = [
        migrations.CreateModel(
            name="TrainingCourse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, unique=True)),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("status_text", models.TextField()),
                ("date_published", models.DateTimeField(null=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="TrainingCourseSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, unique=True)),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("status_text", models.TextField()),
                (
                    "preparation",
                    models.CharField(
                        choices=[
                            ("TODO", "↗"),
                            ("IN_PROGRESS", "~"),
                            ("IN_VALIDATION", "⌛"),
                            ("ON_HOLD", "|"),
                            ("COMPLETED", "✓"),
                            ("STOPPED", "✗"),
                            ("WHEN_FREE", "☴"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "course_media_raw",
                    models.CharField(
                        choices=[
                            ("TODO", "↗"),
                            ("IN_PROGRESS", "~"),
                            ("IN_VALIDATION", "⌛"),
                            ("ON_HOLD", "|"),
                            ("COMPLETED", "✓"),
                            ("STOPPED", "✗"),
                            ("WHEN_FREE", "☴"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "course_media_final",
                    models.CharField(
                        choices=[
                            ("TODO", "↗"),
                            ("IN_PROGRESS", "~"),
                            ("IN_VALIDATION", "⌛"),
                            ("ON_HOLD", "|"),
                            ("COMPLETED", "✓"),
                            ("STOPPED", "✗"),
                            ("WHEN_FREE", "☴"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "course_media_validated",
                    models.CharField(
                        choices=[
                            ("TODO", "↗"),
                            ("IN_PROGRESS", "~"),
                            ("IN_VALIDATION", "⌛"),
                            ("ON_HOLD", "|"),
                            ("COMPLETED", "✓"),
                            ("STOPPED", "✗"),
                            ("WHEN_FREE", "☴"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "implemented_in_app",
                    models.CharField(
                        choices=[
                            ("TODO", "↗"),
                            ("IN_PROGRESS", "~"),
                            ("IN_VALIDATION", "⌛"),
                            ("ON_HOLD", "|"),
                            ("COMPLETED", "✓"),
                            ("STOPPED", "✗"),
                            ("WHEN_FREE", "☴"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "ready_for_whats_and_gram",
                    models.CharField(
                        choices=[
                            ("TODO", "↗"),
                            ("IN_PROGRESS", "~"),
                            ("IN_VALIDATION", "⌛"),
                            ("ON_HOLD", "|"),
                            ("COMPLETED", "✓"),
                            ("STOPPED", "✗"),
                            ("WHEN_FREE", "☴"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "in_sales_funnel",
                    models.CharField(
                        choices=[
                            ("TODO", "↗"),
                            ("IN_PROGRESS", "~"),
                            ("IN_VALIDATION", "⌛"),
                            ("ON_HOLD", "|"),
                            ("COMPLETED", "✓"),
                            ("STOPPED", "✗"),
                            ("WHEN_FREE", "☴"),
                        ],
                        max_length=50,
                    ),
                ),
                ("date_published", models.DateTimeField(null=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app.trainingcourse",
                    ),
                ),
            ],
        ),
    ]
