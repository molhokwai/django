# Generated by Django 5.1.5 on 2025-02-13 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_chatpromptandresponse_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatpromptandresponse',
            name='add_history',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chatpromptandresponse',
            name='history',
            field=models.TextField(blank=True, null=True),
        ),
    ]
