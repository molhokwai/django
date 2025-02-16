from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

import markdown


# ----------------
# AI GUIDANCE JOURNAL
# - Chat prompts and responses
# ----------------
class ChatPromptAndResponse(models.Model):
    """
    Model to store chat prompts and responses.
    """

    # main fields
    prompt = models.TextField()  # Required field
    response = models.TextField(blank=True, null=True)  # Optional field
    think = models.TextField(blank=True, null=True)  # Optional field

    # history fields
    add_history = models.BooleanField(blank=True, null=True)  # Optional field
    history = models.TextField(blank=True, null=True)  # Optional field

    # user fields
    # user = models.ForeignKey(User, null=True, blank=True, 
    #                         on_delete=models.CASCADE,
    #                         related_name="user_chatpromptresponses", editable=False)
    user_id = models.IntegerField(null=True, blank=True, editable=False)  # Optional field

    # crud datetimes
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prompt: {self.prompt[:50]}..."

    class Meta:
        ordering = ["-created_on"]  # Order by most recent first


    def convert_user_id_to_object(self):
        # if self.user is not None \
        #         and not isinstance(self.user, User):  
        #     # Fetch and set user object if user id primitive passed
        #     # -----------------------------------------------------
        #     self.user = User.objects.get(pk=int(self.user))
        #       
        #      @ToDo :: Fix issue, see video: 
        #           https://drive.google.com/file/d/1-xDg4ZPc15gH3taqt\
        #                                   fOJODmp2FC1_5Ok/view?usp=sharing       
        pass


    def convert_markdowns_to_html(self):
        # Convert question and response markdowns to html
        # -----------------------------------------------
        if self.prompt:
            self.prompt = markdown.markdown(self.prompt)
        if self.response:
            self.response = markdown.markdown(self.response)
        if self.think:
            self.think = markdown.markdown(self.think)
