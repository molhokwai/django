from django.shortcuts import render
from .models import Blog


def index(request):
    view_name = "darklight_index"
    template_rel_path = "darklight/index.html"
    context = {}

    context["blogs"] = ["dark", "light"]
    return render(request, template_rel_path, context)
