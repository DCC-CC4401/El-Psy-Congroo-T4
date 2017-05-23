from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request, 'main/base.html', {})

def login(request):
    return render(request, 'main/login.html', {})

