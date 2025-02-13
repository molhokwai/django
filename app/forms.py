from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User



class LoginForm(AuthenticationForm):
    """
    Form for user login.
    """
    username = forms.CharField(label="Email or Phone Number")
    password = forms.CharField(widget=forms.PasswordInput)



class RegisterForm(UserCreationForm):
    """
    Form for user registration.
    """
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ("email", "phone_number", "password1", "password2")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone_number = cleaned_data.get("phone_number")

        if not email and not phone_number:
            raise ValidationError("You must provide either an email or a phone number.")

        return cleaned_data
