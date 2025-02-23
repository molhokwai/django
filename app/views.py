from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from.forms import LoginForm,RegisterForm
from django_app.settings import LOGIN_REDIRECT_URL,LOGOUT_REDIRECT_URL
def index(request):return render(request,'app/index.html',{})
def login_view(request):
	'\n    Handles user login.\n    ';C='Invalid email/phone or password.';A=request
	if A.method=='POST':
		B=LoginForm(A,data=A.POST)
		if B.is_valid():
			E=B.cleaned_data.get('username');F=B.cleaned_data.get('password');D=authenticate(username=E,password=F)
			if D is not None:login(A,D);messages.success(A,'Logged in successfully!');return redirect(LOGIN_REDIRECT_URL)
			else:messages.error(A,C)
		else:messages.error(A,C)
	else:B=LoginForm()
	return render(A,'app/login.html',{'form':B})
def register_view(request):
	'\n    Handles user registration.\n    ';A=request
	if A.method=='POST':
		B=RegisterForm(A.POST)
		if B.is_valid():C=B.save();messages.success(A,'Registration successful! Please log in.');return redirect('login')
		else:messages.error(A,'Registration failed. Please check the form.')
	else:B=RegisterForm()
	return render(A,'app/register.html',{'form':B})
def logout_view(request):'\n    Handles user logout.\n    ';A=request;logout(A);messages.success(A,'Logged out successfully!');return redirect(LOGOUT_REDIRECT_URL)
def journal(request):return render(request,'app/journal.html',{})
def error(request):return render(request,'app/error.html',{})
def test_ollama_raw(request):return render(request,'app/test_ollama.raw.html',{})