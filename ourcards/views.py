from django.shortcuts import render

def index(request):
    view_name = "ourcards_index"
    template_rel_path = "ourcards/index.html"
    context = {}

    return render(request, template_rel_path, context)

