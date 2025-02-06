from django.shortcuts import render
from webapp.models import Article

def home_view(request):
    return render(request, "articles/index.html")

