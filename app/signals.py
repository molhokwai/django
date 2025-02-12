from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:  # Only set username if it's not already set
        if instance.email:
            instance.username = instance.email
        elif hasattr(instance, 'phone_number') and instance.phone_number:
            instance.username = instance.phone_number
        else:
            raise ValidationError("Either an email or phone number must be provided to set a username.")
