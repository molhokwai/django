# Generated by Django 5.1.5 on 2025-01-28 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("webscraping", "0003_webscrape_task_progress_alter_webscrape_website_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="webscrape",
            name="task_progress",
            field=models.IntegerField(default=0, max_length=3),
        ),
    ]
