# Generated by Django 5.1.5 on 2025-02-13 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_chatpromptandresponse_think'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatpromptandresponse',
            name='user',
        ),
        migrations.AddField(
            model_name='chatpromptandresponse',
            name='user_id',
            field=models.IntegerField(blank=True, editable=False, null=True),
        ),
    ]
