from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

import markdown


# ----------------
# GENERAL CONFIG DATA
# - General configuration data storage
# ----------------
class GeneralConfig(models.Model):
    """
        Model to store general config data in a flexible JSON format.

        Fields:
            - title: A title for the general config data.
            - description: A description of general config data and its purpose.
            - json_data: A JSON field to store flexible general config data.
            - created_on: The date and time when the record was created.
            - last_modified: The date and time when the record was last modified.

        Purpose:
            This model is designed to store general config data in a flexible JSON format,
            allowing for easy storage and retrieval of structured or unstructured data.
            It can be used to save data such as:
                - Global config data
                - Application scop config data
                - ...

        With:
            Deepseek AI - "Django/Python" conversation → Mon 10 Feb 2025
    """

    # Title and Description
    title = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        default="General config data..."
    )
    description = models.TextField(
        null=True,
        blank=True,
        default="""
            Storing general config data in a flexible JSON format,
            allowing for easy storage and retrieval of structured or unstructured data.
            It can be used to save data such as:
                - Global config data
                - Application scop config data
            The JSON format allows for flexible storage and easy retrieval of the data.
        """
    )

    # JSON Data Field
    json_data = models.JSONField(
        null=True,
        blank=True,
        default=dict,
        help_text="Flexible JSON field to store general config data."
    )

    # CRUD Datetimes
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)



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


