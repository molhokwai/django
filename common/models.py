from django.db import models
from django.utils.translation import gettext_lazy as _


from django.utils import timezone
from django.utils.crypto import get_random_string
import string, random, datetime
from django.utils.text import slugify 

import os, uuid

def two_days_hence():
    """
    Duplicate. Kept for migration history issue...
    """
    return timezone.now() + timezone.timedelta(days=2)


class Util:
    @staticmethod
    def two_days_hence():
        return timezone.now() + timezone.timedelta(days=2)


    @staticmethod
    def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
        return ''.join(random.choice(chars) for _ in range(size)) 

     
    @staticmethod
    def unique_slug_generator(instance, new_slug = None):
        if new_slug is not None: 
            slug = new_slug 
        else: 
            slug = slugify(instance.title)

        Klass = instance.__class__ 
        max_length = Klass._meta.get_field('slug').max_length 
        slug = slug[:max_length] 
        qs_exists = Klass.objects.filter(slug = slug).exists() 
          
        if qs_exists: 
            new_slug = "{slug}-{randstr}".format( 
                slug = slug[:max_length-5], randstr = Util.random_string_generator(size = 4)) 
                  
            return Util.unique_slug_generator(instance, new_slug = new_slug) 
        return slug

     
    @staticmethod
    def get_unique_filename(filename, folder_path='', slugified=True, token=None, title=None, extension=None):
        """
            Saves an uploaded file with a unique name within a specified folder.

            Args:
              filename (str): The filename.
              folder_path (str, optional): The path to the folder for saving the file (defaults to '').
              slugified (bool, optional): Whether to slugify the file name or not.

            Returns:
              The saved YourModel instance (assuming the file is attached to a model field) or None on error.
        """
        name, ext = os.path.splitext(filename)
        ext = extension if not ext and extension else ext

        token_val = '' if not token else '-%s' % token
        title_val = '' if not title else '-%s' % title
        
        slug = f"{name}{token_val}{title_val}"
        if slugified:
            # Generate a unique slug for the filename
            slug = slugify(slug)

        # Create a unique filename with extension, ensure uniqueness with uuid
        unique_filename = f"{slug}-{str(uuid.uuid4())}{ext}"

        return unique_filename


    @staticmethod
    def unique_random_string(Model, field, l=6):
        # https://stackoverflow.com/questions/26030811/generate-a-unique-string-in-python-django
        key = None
        while True:
            key = get_random_string(l, allowed_chars=string.ascii_uppercase + string.digits) 
            if not Model.objects.filter(**{field:key}).exists():
                break
        return key


    @staticmethod
    def generate_random_password(length=6):
        """Generates a random password of the specified length."""
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def get_user_choices(users):
        return  list(set([(user.id, f"{user.first_name.lower().capitalize()} {user.last_name.upper()}")  \
                                             for user in users]))
