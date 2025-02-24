
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm

from django_app.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL


# -----------
# INDEX, HOME
# -----------
def index(request):

    from app.models import GeneralConfig

    objects = GeneralConfig.objects.all()
    if not len(objects):
        obj = GeneralConfig.objects.create(
            json_data={ 
                'middleware': {
                    'default_image': {
                        'get_interval': 86400
                    }
                }
            }
        )
    else:
        print(f"GeneralConfig.objects.first().json_data: {GeneralConfig.objects.first().json_data}")

    return render(request, "app/index.html", {})



# -----------
# AUTH
# -----------
def login_view(request):
    """
    Handles user login.
    """
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect(LOGIN_REDIRECT_URL)
            else:
                messages.error(request, "Invalid email/phone or password.")
        else:
            messages.error(request, "Invalid email/phone or password.")
    else:
        form = LoginForm()
    return render(request, "app/login.html", {"form": form})


def register_view(request):
    """
    Handles user registration.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")
        else:
            messages.error(request, "Registration failed. Please check the form.")
    else:
        form = RegisterForm()
    return render(request, "app/register.html", {"form": form})


def logout_view(request):
    """
    Handles user logout.
    """
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect(LOGOUT_REDIRECT_URL)


# -----------
# APP
# -----------
def journal(request):
    return render(request, "app/journal.html", {})


# -----------
# HANDLERS
# -----------
def error(request):
    return render(request, "app/error.html", {})





def test_ollama_raw(request):
    return render(request, "app/test_ollama.raw.html", {})

