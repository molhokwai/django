from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from app.models import ChatPromptAndResponse
User=get_user_model()
@receiver(pre_save,sender=User)
def set_username(sender,instance,**B):
	A=instance
	if not A.username:
		if A.email:A.username=A.email
		elif hasattr(A,'phone_number')and A.phone_number:A.username=A.phone_number
		else:raise ValidationError('Either an email or phone number must be provided to set a username.')
@receiver(pre_save,sender=ChatPromptAndResponse)
def set_user_object(sender,instance,**B):A=instance;A.convert_user_id_to_object();A.convert_markdowns_to_html()