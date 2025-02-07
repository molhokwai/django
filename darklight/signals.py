from django.db.models.signals import pre_save, post_save 
from django.dispatch import receiver 


from common.models import Util
from .models import Category, Blog, BlogPost


@receiver(pre_save, sender=Category) 
def pre_save_receiver(sender, instance, *args, **kwargs): 
   # Save once, on create → Clear field to force re-saving
   if not instance.slug: 
       instance.slug = Util.unique_slug_generator(instance) 


@receiver(pre_save, sender=Blog) 
def pre_save_receiver(sender, instance, *args, **kwargs): 
   # Save once, on create → Clear field to force re-saving
   if not instance.slug: 
       instance.slug = Util.unique_slug_generator(instance) 


@receiver(post_save, sender=BlogPost)
def set_image_upload_path(sender, instance, created, **kwargs):
  """
  Signal handler to set upload path for BlogPost images.

  Args:
      sender (BlogPost): The BlogPost model class.
      instance (BlogPost): The BlogPost instance being saved.
      created (bool): Whether the instance is newly created.
      **kwargs: Additional arguments passed to the signal.
  Src:
      https://g.co/gemini/share/714f7b987452

  @ToDo:
      Debug, even though it should not be implemented, 
      unless also changing the upload_to field at image load time...
  """
  # if instance.images.count() > 0:
  #   for image in instance.images.all():
  #       image = instance.images.first()
  #       image.image_file.url = f"/img/cover_images/blogpost/{instance.id}/{image.image_file.name}"
  #       image.save()
  pass


@receiver(pre_save, sender=BlogPost) 
def pre_save_receiver(sender, instance, *args, **kwargs): 
   # Save once, on create → Clear field to force re-saving
   if not instance.slug: 
       instance.slug = Util.unique_slug_generator(instance) 
