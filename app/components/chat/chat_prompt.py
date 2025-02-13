from django_unicorn.components import UnicornView
from app.models import ChatPromptAndResponse


class ChatPromptView(UnicornView):
    """
    Saves a new chat prompt if the user is authenticated.
    """
    prompt = ""
    chatPromptAndResponse: ChatPromptAndResponse = None

    def save_prompt(self):
        """
            Saves the chat prompt to the database
            linking user if authenticated.
        """
        cleaned_prompt = self.prompt.strip()
        
        if cleaned_prompt:
            if self.request.user.is_authenticated:
                self.chatPromptAndResponse = \
                            ChatPromptAndResponse.objects.create(
                                prompt=cleaned_prompt, user=self.request.user)
            else:
                self.chatPromptAndResponse = \
                            ChatPromptAndResponse.objects.create(
                                                prompt=cleaned_prompt)


            # Reload chat list from parent (if corr. method exists)
            # -------------------------------------
            self.reload_chats(self)


    def update_prompt_response(self, _response: str = None, id: int = None):
        """
            Updates the saved chat prompt's response in the database.
            Args are optional, can be called (by front or other view) to save object...

            FUNCTINO TO BE REMOVED !!! 
        """        
        if id:
            chatPromptAndResponse = \
                        ChatPromptAndResponse.objects.get(id=id)
            chatPromptAndResponse.response = _response
            chatPromptAndResponse.save()

        else:
            self.chatPromptAndResponse.response = _response
            self.chatPromptAndResponse.save()

        # Reload chat list from parent (if corr. method exists)
        # -------------------------------------
        self.reload_chats(self)


    def reload_chats(self, force_render=True):
        # Reload chat list from parent (Ensure `load_chats` exists)
        # -------------------------------------
        if self.parent and hasattr(self.parent, "load_chats"):
            print('self.parent and hasattr(self.parent, "load_chats"): TRUE')
            self.parent.load_chats(force_render=force_render)


