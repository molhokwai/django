from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class ChatPromptAndResponse(models.Model):
    """
    Model to store chat prompts and responses.
    """
    prompt = models.TextField()  # Required field
    response = models.TextField(blank=True, null=True)  # Optional field
    user = models.ForeignKey(User, null=True, blank=True, 
                            on_delete=models.CASCADE,
                            related_name="user_chatpromptresponses", editable=False)

    # crud datetimes
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prompt: {self.prompt[:50]}..."

    class Meta:
        ordering = ["-created_on"]  # Order by most recent first

