from django.shortcuts import render


def index(request):
    context = {}
    return render(request, "main/index.html", context)


def test(request):
    context = {}
    return render(request, "main/test.html", context)
