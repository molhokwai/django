from django.db.models import Q

from django_unicorn.components import UnicornView
from app.models import ChatPromptAndResponse
from django_app.settings import (
    AI_JOURNAL_GUIDANCE_CHAT_HISTORY_RECALL as RECALL_CHATS
)
from urllib.parse import parse_qs




class ChatPromptView(UnicornView):
    """
    Saves a new chat prompt if the user is authenticated.
    """
    prompt = ""
    add_history = False
    chatPromptAndResponse: ChatPromptAndResponse = None


    def create_prompt(self):
        """
            Saves the chat prompt to the database
            linking user if authenticated.
        """
        cleaned_prompt = self.prompt.strip()

        history = None
        if self.add_history:
            history = self.make_history()

        if cleaned_prompt:
            if self.request.user.is_authenticated:
                self.chatPromptAndResponse = \
                            ChatPromptAndResponse.objects.create(
                                prompt=cleaned_prompt,
                                add_history=self.add_history,
                                history=history,
                                user_id=self.request.user.id)
            else:
                self.chatPromptAndResponse = \
                            ChatPromptAndResponse.objects.create(
                                            prompt=cleaned_prompt,
                                            history=history,
                                            add_history=self.add_history)


            # Reload chat list from parent (if corr. method exists)
            # -------------------------------------
            self.reload_chats(self)


    def update_prompt(
            self,
            query_string: str = None,
            _response: str = None,
            think: str = None,
            id: int = None):
        """
            Updates the saved chat prompt's response in the database.

            Args are optional, can be called (by front or other view) 
            to save populated object... 

            query_string
                A url parameters like query string variables,
                Workaround to bypass Unicorn multiple arguments js call issue...
                @ToDo :: Fix in Unicorn framework (branch?)
        """

        # Convert query string back to dictionary
        # ---------------------------------------
        parsed_dict = None
        if query_string:
            parsed_dict = {k: v[0] \
                    for k, v in parse_qs(query_string).items()}

        modelObj = self.chatPromptAndResponse
        if id:
            modelObj = ChatPromptAndResponse.objects.get(id=id)

        modelObj.convert_user_id_to_object()
        modelObj = ChatPromptView.\
                    _set_qs_variables(modelObj, parsed_dict)
        modelObj.save()

        if not id:
            self.chatPromptAndResponse = modelObj

        # Reload chat list from parent (if corr. method exists)
        # -------------------------------------
        self.reload_chats()


    def get_history(self):
        """
            Gets the history from self.chatPromptAndResponse
            or generates and returns it.
        """
        history = self.chatPromptAndResponse.history
        if not history:
            history = self.make_history()

        return history



    def make_history(self):
        """
            Generates the user's history and returns it
        """
        Query = Q(user_id=self.request.user.id)
        chatHistoryRows = ChatPromptAndResponse.objects\
                                    .filter(Query)\
                                        .order_by("-created_on")[:RECALL_CHATS]

        history = '\n\n\n'.join(
            list(map(lambda c: \
                f"me: {c.prompt} \n\n you:{c.response}", chatHistoryRows)))

        return history



    @staticmethod
    def _set_qs_variables(
            modelObj: ChatPromptAndResponse, 
            parsed_dict: dict
        ) -> ChatPromptAndResponse:

        if parsed_dict and "_response" in parsed_dict:
            modelObj.response = parsed_dict["_response"]
        if parsed_dict and "think" in parsed_dict:
            modelObj.think = parsed_dict["think"]

        return modelObj


    def reload_chats(self, force_render=True):
        # Reload chat list from parent (Ensure `load_chats` exists)
        # -------------------------------------
        if self.parent and hasattr(self.parent, "load_chats"):
            print('self.parent and hasattr(self.parent, "load_chats"): TRUE')
            self.parent.load_chats(force_render=force_render)


