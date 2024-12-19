# Generated by Django 4.2.11 on 2024-07-12 14:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Le nom/titre de la catégorie ici...', max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('description', tinymce.models.HTMLField(blank=True, null=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime(2024, 7, 12, 14, 8, 34, 919746, tzinfo=datetime.timezone.utc))),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='Le nom/titre de l’image ici...', max_length=200, null=True, unique=True)),
                ('description', tinymce.models.HTMLField(blank=True, default='La description ici...', null=True)),
                ('image_file', models.ImageField(default='/static/templates/main/img/cover_images/post/choose-and-image-fr.png', upload_to='img/unsorted')),
                ('date_uploaded', models.DateTimeField(default=datetime.datetime(2024, 7, 12, 14, 8, 34, 919171, tzinfo=datetime.timezone.utc))),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_admin', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ['date_uploaded'],
            },
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Le titre du post ici...', max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('description', tinymce.models.HTMLField(default='Le contenu ici...')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2024, 7, 12, 14, 8, 34, 920846, tzinfo=datetime.timezone.utc))),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_admin', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_category', to='darklight.category')),
                ('editors', models.ManyToManyField(blank=True, null=True, related_name='blogpost_editors', to=settings.AUTH_USER_MODEL)),
                ('images', models.ManyToManyField(blank=True, null=True, related_name='blogpost_image', to='darklight.image')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Le titre du post ici...', max_length=200, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('description', tinymce.models.HTMLField(default='Le contenu ici...')),
                ('date_created', models.DateTimeField(default=datetime.datetime(2024, 7, 12, 14, 8, 34, 920070, tzinfo=datetime.timezone.utc))),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_admin', to=settings.AUTH_USER_MODEL)),
                ('editors', models.ManyToManyField(blank=True, null=True, related_name='blog_editors', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_created'],
            },
        ),
    ]