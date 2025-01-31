# Generated by Django 5.1.5 on 2025-01-31 01:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("webscraping", "0011_webscrape_by_list_alter_webscrape_task_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="webscrape",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="webscrape_children",
                to="webscraping.webscrape",
            ),
        ),
    ]
