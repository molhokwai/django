_A=None
from django.db.models import Q
from django_unicorn.components import UnicornView
from app.models import ChatPromptAndResponse
from django_app.settings import AI_JOURNAL_GUIDANCE_CHAT_HISTORY_RECALL as RECALL_CHATS
from urllib.parse import parse_qs
class ChatPromptView(UnicornView):
	'\n    Saves a new chat prompt if the user is authenticated.\n    ';prompt='';add_history=False;chatPromptAndResponse:ChatPromptAndResponse=_A
	def create_prompt(A):
		'\n            Saves the chat prompt to the database\n            linking user if authenticated.\n        ';B=A.prompt.strip();C=_A
		if A.add_history:C=A.make_history()
		if B:
			if A.request.user.is_authenticated:A.chatPromptAndResponse=ChatPromptAndResponse.objects.create(prompt=B,add_history=A.add_history,history=C,user_id=A.request.user.id)
			else:A.chatPromptAndResponse=ChatPromptAndResponse.objects.create(prompt=B,history=C,add_history=A.add_history)
			A.reload_chats(A)
	def update_prompt(B,query_string=_A,_response=_A,think=_A,id=_A):
		"\n            Updates the saved chat prompt's response in the database.\n\n            Args are optional, can be called (by front or other view) \n            to save populated object... \n\n            query_string\n                A url parameters like query string variables,\n                Workaround to bypass Unicorn multiple arguments js call issue...\n                @ToDo :: Fix in Unicorn framework (branch?)\n\n                From javascript:\n                    ```js\n                        //* Convert object to query string\n                        const params = { _response, think };\n                        const queryString = new URLSearchParams(params).toString();\n                    ```\n        ";C=query_string;D=_A
		if C:D={A:B[0]for(A,B)in parse_qs(C).items()}
		A=B.chatPromptAndResponse
		if id:A=ChatPromptAndResponse.objects.get(id=id)
		A.convert_user_id_to_object();A=ChatPromptView._set_qs_variables(A,D);A.save()
		if not id:B.chatPromptAndResponse=A
		B.reload_chats()
	def get_history(B):
		'\n            Gets the history from self.chatPromptAndResponse\n            or generates and returns it.\n        ';A=B.chatPromptAndResponse.history
		if not A:A=B.make_history()
		return A
	def make_history(A):"\n            Generates the user's history and returns it\n        ";B=Q(user_id=A.request.user.id);C=ChatPromptAndResponse.objects.filter(B).order_by('-created_on')[:RECALL_CHATS];D='\n\n\n'.join(list(map(lambda c:f"me: {c.prompt} \n\n you:{c.response}",C)));return D
	@staticmethod
	def _set_qs_variables(modelObj,parsed_dict):
		C='think';D='_response';B=modelObj;A=parsed_dict
		if A and D in A:B.response=A[D]
		if A and C in A:B.think=A[C]
		return B
	def reload_chats(A,force_render=True):
		if A.parent and hasattr(A.parent,'load_chats'):print('self.parent and hasattr(self.parent, "load_chats"): TRUE');A.parent.load_chats(force_render=force_render)