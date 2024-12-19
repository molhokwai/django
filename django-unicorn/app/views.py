from django.shortcuts import render


def index(request):
    return render(request, "app/index.html", {})

def start(request):
    return render(request, "app/start.html", {})



def hello_world(request):
    context = {"hello": {"world": {"name": "Galaxy"}}}
    
    return render(request, "app/hello_world.html", context)


def books_demo(request):
    context = {"book": {"Underworld": {"author": "Don DeLillo", "date_published": "1997-05-15"}}}
    
    return render(request, "app/books.html", context)

