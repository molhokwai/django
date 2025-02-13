from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from app.models import ChatPromptAndResponse

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


@receiver(pre_save, sender=ChatPromptAndResponse)
def set_user_object(sender, instance, **kwargs):
    # Fetch and set user object if user id primitive passed
    # -----------------------------------------------------
    instance.convert_user_id_to_object()

    # Convert question and response markdowns to html
    # -----------------------------------------------
    instance.convert_markdowns_to_html()


