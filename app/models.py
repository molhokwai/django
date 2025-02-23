_A=True
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import markdown
class ChatPromptAndResponse(models.Model):
	'\n    Model to store chat prompts and responses.\n    ';prompt=models.TextField();response=models.TextField(blank=_A,null=_A);think=models.TextField(blank=_A,null=_A);add_history=models.BooleanField(blank=_A,null=_A);history=models.TextField(blank=_A,null=_A);user_id=models.IntegerField(null=_A,blank=_A,editable=False);created_on=models.DateTimeField(auto_now_add=_A);last_modified=models.DateTimeField(auto_now=_A)
	def __str__(A):return f"Prompt: {A.prompt[:50]}..."
	class Meta:ordering=['-created_on']
	def convert_user_id_to_object(A):0
	def convert_markdowns_to_html(A):
		if A.prompt:A.prompt=markdown.markdown(A.prompt)
		if A.response:A.response=markdown.markdown(A.response)
		if A.think:A.think=markdown.markdown(A.think)