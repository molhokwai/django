_A='phone_number'
from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
class LoginForm(AuthenticationForm):'\n    Form for user login.\n    ';username=forms.CharField(label='Email or Phone Number');password=forms.CharField(widget=forms.PasswordInput)
class RegisterForm(UserCreationForm):
	'\n    Form for user registration.\n    ';email=forms.EmailField(required=False);phone_number=forms.CharField(max_length=15,required=False)
	class Meta:model=User;fields='email',_A,'password1','password2'
	def clean(D):
		A=super().clean();B=A.get('email');C=A.get(_A)
		if not B and not C:raise ValidationError('You must provide either an email or a phone number.')
		return A