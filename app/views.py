from django.shortcuts import render

def index(request):
    return render(request, "app/index.html", {})

def error(request):
    return render(request, "app/error.html", {})
