from django.shortcuts import render

from webscraping.models import (
    Webscrape, WebscrapeTasks, WebsiteUrls,
    Countries, USStates,
    TaskHandler
)

def index(request):

    taskProgress = TaskHandler.get_taskProgress("feac75b2-df0b-11ef-9114-3db3d945fffd")
    print('------------| taskProgress :: ', taskProgress)

    return render(request, "app/index.html", {})

def start(request):
    return render(request, "app/start.html", {})



def hello_world(request):
    context = {"hello": {"world": {"name": "Galaxy"}}}
    
    return render(request, "app/hello_world.html", context)


def books_demo(request):
    context = {"book": {"Underworld": {"author": "Don DeLillo", "date_published": "1997-05-15"}}}
    
    return render(request, "app/books.html", context)



def trainings_dashboard(request):
    context = {}
    
    return render(request, "app/trainings_dashboard.html", context)

