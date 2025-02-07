# Generated by Django 4.2.11 on 2024-04-03 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('date_published', models.DateField(null=True)),
                ('country', models.CharField(choices=[('CM', 'Cameroon'), ('CA', 'Canada'), ('FR', 'France'), ('NG', 'Nigeria'), ('US', 'USA')], max_length=2, null=True)),
            ],
        ),
    ]
