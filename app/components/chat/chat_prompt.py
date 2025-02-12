from django_unicorn.components import UnicornView
from app.models import ChatPromptAndResponse


class ChatPromptView(UnicornView):
    """
    Saves a new chat prompt if the user is authenticated.
    """
    prompt = ""

    def save_prompt(self):
        """
        Saves the chat prompt to the database only if the user is authenticated.
        """
        cleaned_prompt = self.prompt.strip()
        
        if cleaned_prompt:
            ChatPromptAndResponse.objects.create(prompt=cleaned_prompt, user=self.request.user)

            # Clear the input field
            # Call frontend event (Ensure `onPromptRespondedTo` exists)
            # -------------------------------------
            self.prompt = ""
            self.call("onPromptRespondedTo")

            # Reload chat list from parent (Ensure `load_chats` exists)
            # -------------------------------------
            if self.parent and hasattr(self.parent, "load_chats"):
                print('self.parent and hasattr(self.parent, "load_chats"): TRUE')
                self.parent.load_chats(force_render=True)
