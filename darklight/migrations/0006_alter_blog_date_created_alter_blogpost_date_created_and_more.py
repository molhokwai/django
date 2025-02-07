# Generated by Django 5.1.5 on 2025-01-22 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "darklight",
            "0005_alter_blog_date_created_alter_blogpost_date_created_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 1, 22, 15, 53, 38, 524239, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 1, 22, 15, 53, 38, 532507, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="date_created",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 1, 22, 15, 53, 38, 523883, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="image",
            name="date_uploaded",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2025, 1, 22, 15, 53, 38, 523439, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
