from django.shortcuts import render


def index(request):
    context = {}
    return render(request, "webscraping/index.html", {})


def webscrape(request):
    context = {}
    return render(request, "webscraping/webscrape.html", {})

